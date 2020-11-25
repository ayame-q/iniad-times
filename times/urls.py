from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('article/<int:pk>', views.article, name="article"),
    path('category/<int:category_pk>', views.ListPageView.as_view(), name="category"),
    path('search', views.ListPageView.as_view(), name="search"),
    path('staff/', views.staff, name="staff"),
    path('staff/profile', views.EditStaffProfileView.as_view(), name="profile"),
    path('staff/admin/new', views.AdminNewArticleView.as_view(), name="new_admin"),
    path('staff/admin/list', views.AdminEditListPageView.as_view(), name="list_admin"),
    path('staff/admin/edit/<int:pk>', views.AdminEditArticleView.as_view(), name="edit_admin"),
    path('api/upload_image', views.ApiUploadImage.as_view(), name="post"),
    path('api/parse_markdown', views.ApiParseMarkdown.as_view(), name="parse_markdown"),
]