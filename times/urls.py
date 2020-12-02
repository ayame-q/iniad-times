from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps.views import index as sitemap_index
from . import views
from .sitemaps import ArticleSitemap, CategorySitemap, StaticSitemap

sitemaps = {
    'statics': StaticSitemap,
    'article': ArticleSitemap,
    'categories': CategorySitemap,
}

urlpatterns = [
    path('', views.index, name="index"),
    path('article/<int:pk>', views.article, name="article"),
    path('list', views.ListPageView.as_view(), name="list"),
    path('category/<int:category_pk>', views.ListPageView.as_view(), name="category"),
    path('search', views.ListPageView.as_view(), name="search"),
    path('staff/', views.staff, name="staff"),
    path('staff/new', views.NewPreArticleView.as_view(), name="new"),
    path('staff/edit/list', views.EditPreArticleListView.as_view(), name="edit-list"),
    path('staff/edit/<int:pk>', views.EditPreArticleView.as_view(), name="edit"),
    path('staff/revise/list', views.RevisePreArticleListView.as_view(), name="revise-list"),
    path('staff/revise/<int:pk>', views.RevisePreArticleView.as_view(), name="revise"),
    path('staff/profile', views.EditStaffProfileView.as_view(), name="profile"),
    path('staff/admin/new', views.AdminNewArticleView.as_view(), name="new_admin"),
    path('staff/admin/list', views.AdminEditListPageView.as_view(), name="list_admin"),
    path('staff/admin/edit/<int:pk>', views.AdminEditArticleView.as_view(), name="edit_admin"),
    path('api/get_image_list', views.ApiGetImageList.as_view(), name="get_image_list"),
    path('api/upload_image', views.ApiUploadImage.as_view(), name="upload_image"),
    path('api/parse_markdown', views.ApiParseMarkdown.as_view(), name="parse_markdown"),
    path('api/get_diff', views.ApiGetDiff.as_view(), name="get_diff"),
    path('sitemap.xml', sitemap_index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap")
]