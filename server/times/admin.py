from django.contrib import admin
from .models import User, Staff, Category, Tag, Image, Lecture, PreArticle, Article, BrowsingHistory, RevisionMessage, PreArticleWriterRelation


# Register your models here.
class UserIsStaffFilter(admin.SimpleListFilter):
    title = "スタッフか"
    parameter_name = "staff"

    def lookups(self, request, model_admin):
        return (
            ("true", "スタッフ"),
            ("false", "スタッフでない")
        )

    def queryset(self, request, queryset):
        print(self.value())
        if self.value() is None:
            return queryset
        if self.value() == "true":
            queryset = queryset.exclude(staff=None)
        if self.value() == "false":
            queryset = queryset.filter(staff=None)
        return queryset


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "name", "is_student", "entry_year", "staff")
    list_filter = ("is_student", "entry_year", UserIsStaffFilter)


class StaffAdmin(admin.ModelAdmin):
    list_display = ("slug", "name", "user", "email")
    list_display_links = ("slug", "name", "user", "email")


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "last_staff", "created_at", "publish_at")
    list_display_links = ("id", "title")
    search_fields = ("title", "text", "sns_publish_text", "article_writers", "article_editors", "category", "created_at", "publish_at")


class PreArticleAdmin(PostAdmin):
    list_display = ("id", "title", "format_type", "is_revision_checked", "last_staff", "parent_id", "article_id", "created_at", "publish_at")
    list_filter = ("is_draft", "is_final", "is_revision")

    def format_type(self, obj):
        if obj.is_draft:
            return "下書き"
        if obj.is_final:
            return "最終版"
        if obj.is_revision:
            return f"推敲校閲({obj.revise_count}回目)"


class ArticleAdmin(PostAdmin):
    list_display = ("id", "title", "last_staff", "created_at", "publish_at", "updated_at")


class BrowsingHistoryAdmin(admin.ModelAdmin):
    list_display = ("time", "user", "article")


class PreArticleWriterRelationAdmin(admin.ModelAdmin):
    list_display = ("id", "prearticle_id", "prearticle", "staff")


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Staff, StaffAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Lecture)
admin.site.register(PreArticle, PreArticleAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(BrowsingHistory, BrowsingHistoryAdmin)
admin.site.register(RevisionMessage)
admin.site.register(PreArticleWriterRelation, PreArticleWriterRelationAdmin)
