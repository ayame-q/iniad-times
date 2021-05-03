from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ("family_name", "given_name", "family_name_ruby", "given_name_ruby", "email", "user", "course", "interested_in", "created_at")
    list_display_links = ("family_name", "given_name")


admin.site.register(Profile, ProfileAdmin)
