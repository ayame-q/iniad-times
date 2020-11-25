from django.shortcuts import render, redirect, get_object_or_404, resolve_url
from django.views.generic import UpdateView, DetailView, CreateView, ListView, TemplateView
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.http import Http404
from django.conf import settings
from django.utils import timezone
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from django_boost.views.mixins import ViewUserKwargsMixin
from uuid import uuid4
from datetime import timedelta, date
from .models import Article, Image, Staff, Category
from .markdown import markdown
from . import forms
import os, re


# Create your views here.

class NextUrlMixin(SuccessURLAllowedHostsMixin):
    def get_redirect_url(self):
        redirect_field_name = "next"
        redirect_to = self.request.POST.get(
            redirect_field_name,
            self.request.GET.get(redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''


def is_crawler(request):
    ua = request.META["HTTP_USER_AGENT"]
    if "Googlebot" in ua or "msnbot" in ua or "bingbot" in ua or "Applebot" in ua or "Twitterbot" in ua or "Linespider" in ua or "facebookexternalhit" in ua:
        return True
    return False


def index(request):
    new_articles = Article.objects.order_by("-updated_at").filter(is_posted=True)[:5]
    top_articles = Article.objects.order_by("-updated_at").filter(is_posted=True)[:10]
    is_need_more = Article.objects.order_by("-updated_at").filter(is_posted=True).count() > 10
    data = {
        "new_articles": new_articles,
        "top_articles": top_articles,
        "is_need_more": is_need_more,
        "is_index": True,
    }
    return render(request, "times/index.html", data)


def article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if (not article.is_public and not request.user.is_authenticated) and not is_crawler(request):
        return redirect("/auth/google/login?next=" + request.path)

    if (not article.is_posted) and (not request.user.staff):
        raise Http404

    if request.user.is_authenticated:
        request.user.browsed_histories.create(article=article)

    data = {
        "article": article,
    }
    return render(request, "times/article.html", data)


def staff(request):
    return render(request, "times/staff/index.html")


class AdminNewArticleView(ViewUserKwargsMixin, CreateView):
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
        #url = self.request.build_absolute_uri(resolve_url("detail", pk=data.id))
        return redirect("staff")


class AdminEditArticleView(ViewUserKwargsMixin, UpdateView):
    model = Article
    form_class = forms.AdminArticleForm
    template_name = "times/staff/admin-article.html"

    def form_valid(self, form):
        data = form.save(commit=False)
        data.user = self.request.user
        data.create_ip = get_remote_ip(self.request)
        data.status_ending_at = date.today() + timedelta(weeks=1)
        data.save()
        #url = self.request.build_absolute_uri(resolve_url("detail", pk=data.id))
        return redirect("staff")


class EditStaffProfileView(ViewUserKwargsMixin, UpdateView):
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
            result = Article.objects.order_by("-updated_at").filter(category=category).filter(is_posted=True)
        elif key_word:
            search_result_list = Article.objects.filter(
                Q(title__icontains=key_word) | Q(text__icontains=key_word)
            )
            result = search_result_list.filter(is_posted=True)
        else:
            result = Article.objects.order_by("-updated_at").filter(is_posted=True)
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
        return Response({"data": {"filePath": image.image.url}})


class ApiParseMarkdown(APIView):
    def post(self, request):
        text = request.POST.get("text")
        result = markdown(text, with_toc=True)
        return Response({"text": result})


def get_remote_ip(request):
    forwarded_addresses = request.META.get('HTTP_X_FORWARDED_FOR')
    if forwarded_addresses:
        client_addr = forwarded_addresses.split(',')[0]
    else:
        client_addr = request.META.get('REMOTE_ADDR')
    return client_addr
