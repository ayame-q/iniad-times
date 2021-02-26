from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Staff, Category, Tag, Image, Lecture, PreArticle, Article, BrowsingHistory, RevisionMessage, PreArticleWriterRelation

# Register your models here.
class UserAdmin(BaseUserAdmin):
    def __init__(self, *args, **kwargs):
        fieldsets = list(self.fieldsets)
        fieldsets.append(("個人設定", {
            'fields': ("display_name", "type", "entry_year", "course", "favorite_posts", "favorite_categories", "initialized", "icon_type", "icon_social_model", "profile_text", "profile_url", "profile_twitter", "is_twitter_public", "twitter_token", "twitter_token_secret", "is_tweet_new_question", "line_id", "is_notify_new_answer_on_line", "is_notify_new_supplement_on_line"),
        })),
        self.fieldsets = tuple(fieldsets)
        super().__init__(*args, **kwargs)


# Register your models here.
admin.site.register(User)
admin.site.register(Staff)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Image)
admin.site.register(Lecture)
admin.site.register(PreArticle)
admin.site.register(Article)
admin.site.register(BrowsingHistory)
admin.site.register(RevisionMessage)
admin.site.register(PreArticleWriterRelation)
