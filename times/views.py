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
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django_boost.views.mixins import ViewUserKwargsMixin
from uuid import uuid4
from datetime import timedelta, date, datetime
from .models import Article, PreArticle, Image, Staff, Category
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
        print(year, month)
        print(calendar.monthrange(year, month)[1])
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
                Q(title__icontains=key_word) | Q(text__icontains=key_word)
            )

        if scope == None:
            scope = self.default_scope

        if scope == "all":
            pass
        elif scope == "my-related":
            result = result.filter(
                Q(article_writers=self.request.user.staff) | Q(article_editors=self.request.user.staff)
            )
        elif scope == "mine":
            result = result.filter(last_staff=self.request.user.staff)

        if not old:
            result = result.filter(children=None)

        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["link_page"] = self.link_page
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
        result = result.filter(is_draft=False, articles=None).exclude(article_writers=self.request.user.staff)
        count_0 = [object for object in result.filter(revise_count=0)]
        count_1 = [object for object in result.filter(revise_count=1).exclude(parent__last_staff=self.request.user.staff, parent__revise_count=1) if object.is_writer_check_completed()]
        return count_0 + count_1


class BasePreArticleMixin:
    model = PreArticle
    form_class = forms.PreArticleForm
    template_name = "times/staff/article-form.html"
    is_edit = False
    is_revision = False

    def form_valid(self, form):
        data = form.save(commit=False)
        if self.is_revision:
            data.is_revision = True
        if self.is_edit:
            writers = data.article_writers.all()
            editors = data.article_editors.all()
            data.parent_id = data.id
            data.id = None
            data.uuid = uuid4()
        data.last_staff = self.request.user.staff
        data.create_ip = get_remote_ip(self.request)
        data.status_ending_at = date.today() + timedelta(weeks=1)
        data.save()
        if self.is_edit:
            for writer in writers:
                data.article_writers.add(writer)
            for editor in editors:
                data.article_editors.add(editor)
        if self.is_revision:
            data.article_editors.add(self.request.user.staff)
        else:
            data.article_writers.add(self.request.user.staff)
        #url = self.request.build_absolute_uri(resolve_url("article", pk=data.id))
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
                Q(title__icontains=key_word) | Q(text__icontains=key_word)
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


class ApiGetImageList(ListAPIView):
    queryset = Image.objects.order_by("-id")
    serializer_class = serializers.ImageSerializer


class ApiUploadImage(APIView):
    def post(self, request):
        image_file = request.FILES["image"]
        title = request.POST.get("title")
        _, ext = os.path.splitext(image_file.name)
        if not re.fullmatch("\.(jpe?g|png)", ext):
            return Response({"error": "jpgかpngファイルをアップロードしてください"})
        if not request.user.staff:
            return Response({"error": "権限がありません"})
        image_file.name = str(uuid4()) + ext
        image = Image(image=image_file, staff=request.user.staff, title=title)
        image.save()
        return Response({"data": {"id": image.id, "filePath": image.image.url}})


class ApiParseMarkdown(APIView):
    def post(self, request):
        text = request.POST.get("text")
        result = markdown(text, with_toc=True)
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
