from django.contrib import admin
from .models import Profile, News


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("family_name", "given_name", "family_name_ruby", "given_name_ruby", "email", "user", "course", "interested_in", "created_at")
    list_display_links = ("family_name", "given_name")


class NewsAdmin(admin.ModelAdmin):
    list_display = ("date", "title", "created_at")
    list_display_links = ("date", "title")


admin.site.register(Profile, ProfileAdmin)
admin.site.register(News, NewsAdmin)