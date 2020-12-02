from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.views.generic import UpdateView, DetailView, CreateView, ListView, TemplateView
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from django_boost.views.mixins import ViewUserKwargsMixin
from uuid import uuid4
from datetime import timedelta, date
from .models import Article, PreArticle, Image, Staff, Category
from .markdown import markdown
from . import forms, serializers
from .publish import Publish
import os, re, difflib


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


def article(request, pk):
    article = get_object_or_404(Article, pk=pk)

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


class NewPreArticleView(LoginRequiredMixin, BasePreArticleMixin, CreateView):
    is_edit = False
    is_revision = False
    extra_context = {"is_new_form": True}


class EditPreArticleView(LoginRequiredMixin, BasePreArticleMixin, UpdateView):
    is_edit = True
    is_revision = False


class RevisePreArticleView(LoginRequiredMixin, BasePreArticleMixin, UpdateView):
    is_edit = True
    is_revision = True
    extra_context = {"is_revision_form": True}


class AdminNewArticleView(CreateView):
    model = Article
    form_class = forms.AdminArticleForm
    template_name = "times/staff/admin-article.html"
    extra_context = {"is_new_form": True}

    def form_valid(self, form):
        data = form.save(commit=False)
        data.user = self.request.user
        data.create_ip = get_remote_ip(self.request)
        data.status_ending_at = date.today() + timedelta(weeks=1)
        data.save()
        publish.publish(data)
        #url = self.request.build_absolute_uri(resolve_url("article", pk=data.id))
        return redirect("staff")


class AdminEditArticleView(UpdateView):
    model = Article
    form_class = forms.AdminArticleForm
    template_name = "times/staff/admin-article.html"

    def form_valid(self, form):
        data = form.save(commit=False)
        data.user = self.request.user
        data.create_ip = get_remote_ip(self.request)
        data.status_ending_at = date.today() + timedelta(weeks=1)
        data.save()
        publish.publish(data)
        #url = self.request.build_absolute_uri(resolve_url("article", pk=data.id))
        return redirect("staff")


class EditStaffProfileView(UpdateView):
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


class AdminEditListPageView(ListView):
    model = Article
    context_object_name = "articles"
    template_name = "times/staff/article-list.html"
    paginate_by = 20

    def get_queryset(self):
        category_pk = self.kwargs.get("category_pk")
        key_word = self.request.GET.get("q")
        if category_pk:
            category = Category.objects.get(pk=category_pk)
            result = Article.objects.order_by("-updated_at").filter(category=category)
        elif key_word:
            search_result_list = Article.objects.filter(
                Q(title__icontains=key_word) | Q(text__icontains=key_word)
            )
            result = search_result_list
        else:
            result = Article.objects.order_by("-updated_at")
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
        text = request.POST.get("text").replace("\r\n", "\n").split("\n")
        uuid = request.POST.get("uuid")
        object = None
        object_text = [""]
        try:
            if PreArticle.objects.get(uuid=uuid):
                object = PreArticle.objects.get(uuid=uuid)
                object_text = object.text.replace("\r\n", "\n").split("\n")
            elif Article.objects.get(uuid=uuid):
                object = Article.objects.get(uuid=uuid)
                object_text = object.text.replace("\r\n", "\n").split("\n")
        except ValidationError:
            pass
        print(object_text)
        print(text)
        result = ""
        for line in difflib.ndiff(object_text, text):
            if line[0] == "+":
                line = f"<pre class='diff-line added-line'>{line}</pre>"
            elif line[0] == "-":
                line = f"<pre class='diff-line deleted-line'>{line}</pre>"
            elif line[0] == "?":
                continue
            else:
                line = f"<pre class='diff-line'>{line}</pre>"
            result += line + "\n"
        return Response({"text": result})


def get_remote_ip(request):
    forwarded_addresses = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_addresses:
        client_addr = forwarded_addresses.split(',')[0]
    else:
        client_addr = request.META.get('REMOTE_ADDR')
    return client_addr
