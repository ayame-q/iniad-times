from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.views.generic import UpdateView, DetailView, CreateView, ListView, TemplateView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.conf import settings
from django.utils import timezone
from django.db.models import Q, Count
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from django_boost.views.mixins import ViewUserKwargsMixin
from PIL import Image as PILImage
from uuid import uuid4
from datetime import timedelta, date, datetime
from .models import Article, PreArticle, RevisionMessage, Image, Staff, Category
from .markdown import markdown
from . import forms, serializers
from .publish import Publish
from .get_diff import get_diff
import os, re, calendar


publish = Publish()


def is_crawler(request):
    ua = request.META["HTTP_USER_AGENT"]
    if "Googlebot" in ua or "msnbot" in ua or "bingbot" in ua or "Applebot" in ua or "Twitterbot" in ua or "Linespider" in ua or "facebookexternalhit" in ua:
        return True
    return False


def index(request):
    new_articles = Article.objects.filter(is_publishable=True, publish_at__lt=timezone.localtime()).order_by("-publish_at")[:5]
    top_articles = Article.objects.filter(is_publishable=True, publish_at__lt=timezone.localtime()).order_by("-publish_at")[:10]
    is_need_more = Article.objects.filter(is_publishable=True, publish_at__lt=timezone.localtime()).order_by("-publish_at").count() > 10
    data = {
        "new_articles": new_articles,
        "top_articles": top_articles,
        "is_need_more": is_need_more,
        "is_index": True,
    }
    return render(request, "times/index.html", data)


def article(request, slug=None, year=None, month=None, pk=None, uuid=None):
    article = None
    if slug:
        article = get_object_or_404(Article, slug=slug)
        if not (article.publish_at.year == year and article.publish_at.month == month):
            raise Http404
    if pk or uuid:
        if pk:
            article = get_object_or_404(Article, pk=pk)
        elif uuid:
            article = get_object_or_404(Article, uuid=uuid)
        if article and article.slug:
            permanent = True
            if settings.DEBUG:
                permanent = False
            return redirect("article", article.publish_at.year, article.publish_at.month, article.slug, permanent=permanent)

    if (not article.is_publishable or article.publish_at > timezone.localtime()) and (not request.user.is_authenticated or not request.user.staff):
        raise Http404

    if (not article.is_public and not request.user.is_authenticated) and not is_crawler(request):
        return redirect("/auth/google/login?next=" + request.path)

    if request.user.is_authenticated:
        request.user.browsed_histories.create(article=article)

    data = {
        "article": article,
    }
    return render(request, "times/article.html", data)


def staff(request):
    return render(request, "times/staff/index.html")


class StaffOnlyMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        result = super().dispatch(request, *args, **kwargs)
        if not request.user.staff:
            raise PermissionError
        return result


class GetSingleObjectMixin(SingleObjectMixin):
    def get_object(self, queryset=None):
        try:
            object = super(GetSingleObjectMixin, self).get_object(queryset=queryset)
        except AttributeError:
            uuid = self.kwargs.get("uuid")
            if uuid:
                object = get_object_or_404(self.model, uuid=uuid)
            else:
                raise AttributeError
        return object


class GetArticleAndPreArticleObjectMixin(SingleObjectMixin):
    model = Article # 優先出力モデル
    def get_object(self, queryset=None):
        uuid = self.kwargs.get("uuid")
        pk = self.kwargs.get("pk")
        if uuid:
            object = self.model.objects.get(uuid=uuid)
        else:
            raise AttributeError
        return object


class PreviewPageView(StaffOnlyMixin, GetSingleObjectMixin, DetailView):
    model = PreArticle
    context_object_name = "article"
    template_name = "times/article.html"
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.object.is_revision:
            writers = [f"{ writer.name } &lt;{ writer.user.name }&gt;" for writer in self.object.article_writers.all()]
            context["preview_message"] = f"""推敲/校閲が完了しました。<br>
筆者 ({ ', '.join(writers) }) へ以下の確認用URLを通知してください。<br>
<input type='text' value='https://iniad-wm.com/staff/revise/check/{self.object.uuid}' readonly onclick="this.select()">"""
        return context


class BaseStaffListPageView(ListView):
    model = PreArticle
    context_object_name = "articles"
    template_name = "times/staff/list.html"
    paginate_by = 20
    default_scope = "mine"
    link_page = "edit"
    link_keys = ["uuid"]

    def get_queryset(self):
        key_word = self.request.GET.get("q")
        scope = self.request.GET.get("scope")
        old = self.request.GET.get("old")
        result = self.model.objects.order_by("-created_at")
        if key_word:
            result = result.filter(
                Q(title__icontains=key_word) or Q(text__icontains=key_word)
            )

        if scope == None:
            scope = self.default_scope

        if scope == "all":
            result = result.all()
        elif scope == "my-related":
            result = result.filter(
                Q(article_writers=self.request.user.staff) or Q(article_editors=self.request.user.staff)
            )
        elif scope == "mine":
            result = result.filter(last_staff=self.request.user.staff)

        if not old:
            result = result.filter(children=None)

        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["link_page"] = self.link_page
        scope = self.request.GET.get("scope")
        if not scope:
            scope = self.default_scope
        context["scope"] = scope
        return context


class EditPreArticleListView(StaffOnlyMixin, BaseStaffListPageView):
    extra_context = {"edit_list": True}
    def get_queryset(self):
        result = super(EditPreArticleListView, self).get_queryset()
        return result.filter(is_draft=True)


class RevisePreArticleListView(StaffOnlyMixin, BaseStaffListPageView):
    default_scope = "all"
    link_page = "revise"
    extra_context = {"revise_list": True}

    def get_queryset(self):
        result = super(RevisePreArticleListView, self).get_queryset()
        rejected = [object for object in result.filter(is_revision=True, is_revision_rejected=True, last_staff=self.request.user.staff)]
        my_draft = [object for object in result.filter(is_draft=True, is_revision=True, last_staff=self.request.user.staff)]
        original = result.filter(is_draft=False, is_final=False).exclude(article_writers=self.request.user.staff)
        count_0 = [object for object in original.filter(revise_count=0)]
        count_1 = [object for object in original.filter(revise_count=1, is_revision_checked=True).exclude(article_editors=self.request.user.staff)]
        return rejected + my_draft + count_0 + count_1


class CheckRevisePreArticleListView(StaffOnlyMixin, BaseStaffListPageView):
    default_scope = "all"
    link_page = "check-revise"
    extra_context = {"check_revise_list": True}

    def get_queryset(self):
        result = super(CheckRevisePreArticleListView, self).get_queryset()
        result = result.filter(is_draft=False, is_revision=True, article_writers=self.request.user.staff, is_final=False)
        result = [object for object in result if object.writer_relations.get(staff=self.request.user.staff).writer_check == 0]
        return result


class FinalCheckPreArticleListView(StaffOnlyMixin, BaseStaffListPageView):
    default_scope = "all"
    link_page = "admin-final-check"
    extra_context = {"final_check_list": True}

    def get_queryset(self):
        if not self.request.user.is_superuser:
            raise PermissionError
        result = super(FinalCheckPreArticleListView, self).get_queryset()
        result = result.filter(is_draft=False, is_revision=True, revise_count__gte=2, is_revision_checked=True, is_final=False)
        return result


class ReeditArticleListView(StaffOnlyMixin, BaseStaffListPageView):
    default_scope = "my-related"
    link_page = "reedit"
    extra_context = {"reedit_list": True}
    def get_queryset(self):
        result = super(ReeditArticleListView, self).get_queryset()
        return result.exclude(article=None)


class BasePreArticleMixin:
    model = PreArticle
    form_class = forms.PreArticleForm
    template_name = "times/staff/article-form.html"
    is_edit = False
    is_revision = False
    is_final_check = False
    is_reedit = False

    def form_valid(self, form):
        data = form.save(commit=False)
        if self.is_revision:
            data.is_revision = True
            data.is_revision_rejected = False
            data.is_revision_checked = False
            if not data.is_draft and not data.is_revision_rejected:
                data.revise_count += 1
        if self.is_edit:
            revision_messages = data.revision_messages.all()
            writers = data.article_writers.all()
            editors = data.article_editors.all()
            data.parent_id = data.id
            data.id = None
            data.uuid = uuid4()
        data.is_final = False
        data.last_staff = self.request.user.staff
        data.create_ip = get_remote_ip(self.request)
        data.status_ending_at = date.today() + timedelta(weeks=1)
        data.save()

        if self.is_edit:
            for writer in writers:
                data.article_writers.add(writer)
            for editor in editors:
                data.article_editors.add(editor)
            for message in revision_messages:
                data.revision_messages.add(message)
        if not self.is_final_check:
            if self.is_revision:
                data.article_editors.add(self.request.user.staff)
            else:
                data.article_writers.add(self.request.user.staff)
        message_comment = self.request.POST.get("message-comment")
        if message_comment:
            message = RevisionMessage.objects.create(staff=self.request.user.staff, comment=message_comment)
            data.revision_messages.add(message)

        if self.is_final_check or self.is_reedit:
            method = self.request.POST.get("method")
            if method == "recheck":
                data.is_revision = True
                data.is_revision_rejected = False
                data.is_revision_checked = False
                if self.is_reedit:
                    data.revise_count = 1
                data.save()
            if method == "publish":
                article = data.publish()
                data.is_final = True
                data.save()
        if self.is_revision:
            return redirect("preview", data.uuid)
        return redirect("staff")


class NewPreArticleView(StaffOnlyMixin, BasePreArticleMixin, CreateView):
    is_edit = False
    is_revision = False
    extra_context = {"is_new_form": True}


class EditPreArticleView(StaffOnlyMixin, BasePreArticleMixin, GetSingleObjectMixin, UpdateView):
    is_edit = True
    is_revision = False


class RevisePreArticleView(StaffOnlyMixin, BasePreArticleMixin, GetSingleObjectMixin, UpdateView):
    is_edit = True
    is_revision = True
    extra_context = {"is_revision_form": True}


class CheckReviseView(StaffOnlyMixin, GetSingleObjectMixin, DetailView):
    model = PreArticle
    template_name = "times/staff/article-check.html"
    writer_relation = None

    def get_object(self, queryset=None):
        object = super(CheckReviseView, self).get_object()
        try:
            self.writer_relation = object.writer_relations.get(staff=self.request.user.staff)
        except object.writer_relations.DoesNotExist:
            raise PermissionError
        return object


class FinalCheckPreArticleView(StaffOnlyMixin, BasePreArticleMixin, GetSingleObjectMixin, UpdateView):
    is_edit = True
    is_final_check = True
    extra_context = {"is_final_check_form": True}
    
    def get_object(self, queryset=None):
        if not self.request.user.is_superuser:
            raise PermissionError
        return super(FinalCheckPreArticleView, self).get_object()



class ReeditArticleView(StaffOnlyMixin, BasePreArticleMixin, GetSingleObjectMixin, UpdateView):
    is_edit = True
    is_reedit = True
    extra_context = {"is_reedit_form": True}


class EditStaffProfileView(StaffOnlyMixin, UpdateView):
    model = Staff
    form_class = forms.StaffProfileForm
    template_name = "times/staff/profile.html"

    def get_object(self, queryset=None):
        self.form_class = forms.StaffProfileForm
        return self.request.user.staff


class ListPageView(ListView):
    model = Article
    context_object_name = "articles"
    template_name = "times/list.html"
    paginate_by = 20

    def get_queryset(self):
        category_pk = self.kwargs.get("category_pk")
        key_word = self.request.GET.get("q")
        if category_pk:
            category = Category.objects.get(pk=category_pk)
            result = Article.objects.order_by("-updated_at").filter(category=category).filter(is_publishable=True)
        elif key_word:
            search_result_list = Article.objects.filter(
                Q(title__icontains=key_word) or Q(text__icontains=key_word)
            )
            result = search_result_list.filter(is_publishable=True)
        else:
            result = Article.objects.order_by("-updated_at").filter(is_publishable=True)
        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        category_pk = self.kwargs.get("category_pk")
        if category_pk:
            category = Category.objects.get(pk=category_pk)
            context["category"] = category
        return context


class ApiGetRevisionMessagesView(ListAPIView):
    serializer_class = serializers.RevisionMessageSerializer
    def get_queryset(self):
        uuid = self.request.GET.get("uuid")
        if not uuid:
            raise ValueError
        prearticle = get_object_or_404(PreArticle, uuid=uuid)
        return RevisionMessage.objects.filter(pre_articles=prearticle).order_by("-id")


class ApiCreateRevisionMessageView(CreateAPIView):
    serializer_class = serializers.RevisionMessageSerializer

    def perform_create(self, serializer):
        serializer.save(staff=self.request.user.staff)


class ApiCompleteCheckReviseView(APIView):
    def post(self, request):
        uuid = request.POST["uuid"]
        method = request.POST["method"]
        prearticle = get_object_or_404(PreArticle, uuid=uuid)
        writer_relation = prearticle.writer_relations.get(staff=request.user.staff)
        if method == "reject":
            writer_relation.writer_check = -1
            writer_relation.save()
            prearticle.is_revision_rejected = True
        if method == "accept":
            writer_relation.writer_check = 1
            writer_relation.save()
            if prearticle.is_writer_check_completed():
                prearticle.is_revision_checked = True
        prearticle.save()
        return Response({"method": method, "ok": True})


class ApiGetImageList(ListAPIView):
    queryset = Image.objects.order_by("-id")
    serializer_class = serializers.ImageSerializer


class ApiUploadImage(APIView):
    def post(self, request):
        image_file = request.FILES["image"]
        title = request.POST.get("title")
        _, ext = os.path.splitext(image_file.name)
        if not re.fullmatch("\.(jpe?g|png)", ext.lower()):
            return Response({"error": "jpgかpngファイルをアップロードしてください"})
        if not request.user.staff:
            return Response({"error": "権限がありません"})
        image_file.name = str(uuid4()) + ext.lower()
        image = Image(image=image_file, staff=request.user.staff, title=title)
        image.save()
        return Response({"data": {"id": image.id, "filePath": image.image.large.url}})


class ApiParseMarkdown(APIView):
    def post(self, request):
        text = request.POST.get("text")
        result = markdown(text)
        return Response({"text": result})


class ApiGetDiff(APIView):
    def post(self, request):
        text = request.POST.get("text")
        uuid = request.POST.get("uuid")
        object_text = ""
        try:
            if PreArticle.objects.get(uuid=uuid):
                object = PreArticle.objects.get(uuid=uuid)
                object_text = object.text
            elif Article.objects.get(uuid=uuid):
                object = Article.objects.get(uuid=uuid)
                object_text = object.text
        except ValidationError:
            pass
        result = get_diff(object_text, text)
        return Response({"text": result})


class ApiCheckPreArticleSlugIsUnique(APIView):
    def get(self, request):
        uuid = request.GET.get("uuid")
        slug = request.GET.get("slug")
        if uuid:
            object = PreArticle.objects.get(uuid=uuid)
            is_unique = object.is_slug_unique(slug)
        else:
            is_unique = PreArticle.is_slug_unique_in_class(slug)
        return Response({"is_unique": is_unique})


def get_remote_ip(request):
    forwarded_addresses = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_addresses:
        client_addr = forwarded_addresses.split(',')[0]
    else:
        client_addr = request.META.get('REMOTE_ADDR')
    return client_addr
