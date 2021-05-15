from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, News


class EntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("email", "family_name", "given_name", "family_name_ruby", "given_name_ruby", "course", "interested_in")


class EntryWebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("email", "family_name", "given_name", "family_name_ruby", "given_name_ruby")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("email", "student_id", "get_class")


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ("title", "date")