from django.urls import path, register_converter
from . import views

urlpatterns = [
    path('entry', views.EntryAPIView.as_view(), name="api_entry"),
    path('webhook/entry', views.EntryWebhookAPIView.as_view(), name="api_webhook_entry"),
    path('is_authenticated', views.IsAuthenticatedAPIView.as_view(), name="api_is_authenticated"),
    path('user/mine', views.MyUserAPIView.as_view(), name="api_my_user"),
    path('tutorial', views.CircleTutorialAPIView.as_view(), name="api_tutorial")
]