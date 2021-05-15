from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from . import serializers
from .models import News, Profile
from times.models import Staff
from .sendmail import send_initial_mail
import requests, os, hashlib, json, re


# Create your views here.
class EntryAPIView(CreateAPIView):
    serializer_class = serializers.EntrySerializer

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            return super(EntryAPIView, self).perform_create(serializer)
        serializer.save(user=self.request.user, email=self.request.user.email)
        entry(self.request.user.email)


class EntryWebhookAPIView(CreateAPIView):
    serializer_class = serializers.EntryWebhookSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if not request.META.get("HTTP_AUTHENTICATION"):
            raise PermissionError("No Authentication")
        created_at = json.loads(request.body).get("created_at")
        dat = created_at + os.environ.get("ENTRY_WEBHOOK_PASSWORD")
        token_correct = hashlib.sha256(dat.encode()).hexdigest()
        token_get = re.fullmatch(r"Token (.+)", request.META.get("HTTP_AUTHENTICATION")).group(1)
        if token_correct != token_get:
            raise PermissionError("Token is invalid")
        super(EntryWebhookAPIView, self).post(request=request, *args, **kwargs)

    def perform_create(self, serializer):
        instance = serializer.save()
        entry(instance.email)


def entry(email):
    Staff.objects.create(email=email)
    try:
        add_google_drive(email)
    except Exception as e:
        print(f"Drive Add Error!: {email}")
        print(e)
    send_initial_mail(email)


def add_google_drive(email):
    url = os.environ.get('GOOGLE_DRIVE_GAS_URL')
    password = os.environ.get('GOOGLE_DRIVE_GAS_PASSWORD')
    data = {
        "email": email,
        "password": password
    }
    headers = {
        'Accept': "application/json",
        'Content-Type': "application/x-www-form-urlencoded",
    }
    response = requests.post(
        url,
        data=data,
        headers=headers
    )
    if response.json().get("error"):
        raise ConnectionError
    return response.json().get("email")


class IsAuthenticatedAPIView(APIView):
    def get(self, request):
        return Response({"authenticated": request.user.is_authenticated})


class MyUserAPIView(RetrieveAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class CircleTutorialAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"is_login": False})
        try:
            request.user.profile
        except:
            return Response({"is_login": True, "is_member": False})
        data = {
            "is_login": True,
            "is_member": True,
            "slack_url": os.environ.get("CIRCLE_TUTORIAL_SLACK_URL"),
            "esa_url": os.environ.get("CIRCLE_TUTORIAL_ESA_URL"),
            "discord_url": os.environ.get("CIRCLE_TUTORIAL_DISCORD_URL"),
            "drive_url": os.environ.get("CIRCLE_TUTORIAL_DRIVE_URL"),
            "questionnaire_url": os.environ.get("CIRCLE_TUTORIAL_QUESTIONNAIRE_URL")
        }
        return Response(data)


class NewsListAPIView(ListAPIView):
    serializer_class = serializers.NewsSerializer
    queryset = News.objects.all()


class MemberCountAPIView(APIView):
    def get(self, request):
        member_count = Profile.objects.filter(is_ob_og=False).count()
        return Response({"count": member_count})
