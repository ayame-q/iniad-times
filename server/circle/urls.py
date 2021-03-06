from django.urls import path, register_converter
from . import views

urlpatterns = [
    path('news/', views.NewsListAPIView.as_view(), name="api_news"),
    path('member_count', views.MemberCountAPIView.as_view(), name="api_member_count"),
    path('entry', views.EntryAPIView.as_view(), name="api_entry"),
    path('webhook/entry', views.EntryWebhookAPIView.as_view(), name="api_webhook_entry"),
    path('is_authenticated', views.IsAuthenticatedAPIView.as_view(), name="api_is_authenticated"),
    path('user/mine', views.MyUserAPIView.as_view(), name="api_my_user"),
    path('tutorial', views.CircleTutorialAPIView.as_view(), name="api_tutorial")
]