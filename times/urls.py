from django.urls import path, register_converter
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps.views import index as sitemap_index
from . import views, converters
from .sitemaps import ArticleSitemap, CategorySitemap, StaticSitemap

register_converter(converters.FourDigitYearConverter, 'yyyy')
register_converter(converters.TwoDigitMonthConverter, 'mm')

sitemaps = {
    'statics': StaticSitemap,
    'article': ArticleSitemap,
    'categories': CategorySitemap,
}

urlpatterns = [
    path('', views.index, name="index"),
    path('<yyyy:year>/<mm:month>/<slug:slug>', views.article, name="article"),
    path('article/<int:pk>', views.article, name="article"),
    path('article/<uuid:uuid>', views.article, name="article"),
    path('list', views.ListPageView.as_view(), name="list"),
    path('category/<int:category_pk>', views.ListPageView.as_view(), name="category"),
    path('search', views.ListPageView.as_view(), name="search"),
    path('staff/', views.staff, name="staff"),
    path('staff/new', views.NewPreArticleView.as_view(), name="new"),
    path('staff/edit/', views.EditPreArticleListView.as_view(), name="edit-list"),
    path('staff/edit/<int:pk>', views.EditPreArticleView.as_view(), name="edit"),
    path('staff/edit/<uuid:uuid>', views.EditPreArticleView.as_view(), name="edit"),
    path('staff/revise/', views.RevisePreArticleListView.as_view(), name="revise-list"),
    path('staff/revise/<int:pk>', views.RevisePreArticleView.as_view(), name="revise"),
    path('staff/revise/<uuid:uuid>', views.RevisePreArticleView.as_view(), name="revise"),
    path('staff/revise/check/', views.CheckRevisePreArticleListView.as_view(), name="check-revise-list"),
    path('staff/revise/check/<int:pk>', views.CheckReviseView.as_view(), name="check-revise"),
    path('staff/revise/check/<uuid:uuid>', views.CheckReviseView.as_view(), name="check-revise"),
    path('staff/admin/final_check/', views.FinalCheckPreArticleListView.as_view(), name="admin-final-check-list"),
    path('staff/admin/final_check/<int:pk>', views.FinalCheckPreArticleView.as_view(), name="admin-final-check"),
    path('staff/admin/final_check/<uuid:uuid>', views.FinalCheckPreArticleView.as_view(), name="admin-final-check"),
    path('staff/profile', views.EditStaffProfileView.as_view(), name="profile"),
    path('api/get_image_list', views.ApiGetImageList.as_view(), name="get_image_list"),
    path('api/upload_image', views.ApiUploadImage.as_view(), name="upload_image"),
    path('api/parse_markdown', views.ApiParseMarkdown.as_view(), name="parse_markdown"),
    path('api/get_diff', views.ApiGetDiff.as_view(), name="get_diff"),
    path('api/check_prearticle_slug_is_unique', views.ApiCheckPreArticleSlugIsUnique.as_view(), name="check_prearticle_slug_is_unique"),
    path('api/revision_message/get', views.ApiGetRevisionMessagesView.as_view(), name="get_revision_messages"),
    path('api/revision_message/post', views.ApiCreateRevisionMessageView.as_view(), name="create_revision_message"),
    path('api/complete_check_revise', views.ApiCompleteCheckReviseView.as_view(), name="complete_check_revise"),
    path('sitemap.xml', sitemap_index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', sitemap, {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap")
]