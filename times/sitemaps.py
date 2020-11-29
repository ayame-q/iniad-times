from django.contrib.sitemaps import Sitemap
from django.shortcuts import resolve_url
from django.utils import timezone
from datetime import timedelta
from .models import Article, Category


class ArticleSitemap(Sitemap):
    priority = 0.8
    protocol = "https"

    def items(self):
        return Article.objects.filter(is_publishable=True, publish_at__lt=timezone.localtime()).order_by("-publish_at")

    def location(self, obj):
        return resolve_url('article', pk=obj.pk)

    def lastmod(self, obj):
        return obj.time()

    def changefreq(self, obj):
        if obj.publish_at > timezone.localtime() + timedelta(days=-7):
            return "daily"
        elif obj.publish_at > timezone.localtime() + timedelta(days=-30):
            return "weekly"
        else:
            return "monthly"



class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = "https"

    def items(self):
        return Category.objects.all()

    def location(self, obj):
        return resolve_url('category', category_pk=obj.pk)

    def lastmod(self, obj):
        latest_post = Article.objects.filter(category=obj, is_publishable=True, publish_at__lt=timezone.localtime())[:1]
        if len(latest_post) > 0:
            return latest_post[0].updated_at


class StaticSitemap(Sitemap):
    protocol = "https"

    def items(self):
        return ['index', 'list']

    def location(self, obj):
        return resolve_url(obj)

    def lastmod(self, obj):
        if obj in ['index', 'list']:
            latest_post = Article.objects.filter(is_publishable=True, publish_at__lt=timezone.localtime()).order_by("-publish_at")[:1]
            if len(latest_post) > 0:
                return latest_post[0].updated_at

    def priority(self, obj):
        if obj == 'index':
            return 1.0
        elif obj == 'list':
            return 0.3
        else:
            return 0.1

    def changefreq(self, obj):
        if obj in ['index', 'list']:
            return "hourly"
        else:
            return "monthly"
