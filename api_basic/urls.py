from django.db import router
from django.urls import path
from django.urls.conf import include
from . views import ArticleViewset, article_details, article_list, articleAPIView, articleDetailsView, GenericAPIView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('article',ArticleViewset, basename='article')


urlpatterns = [
    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>/', include(router.urls)),
    path("detail/<int:id>/", articleDetailsView.as_view()),
    path("arti/", articleAPIView.as_view()),
    path("gene/", GenericAPIView.as_view()),
    path("details/<int:pk>/", article_details),
    path("article/", article_list),
    
]




# **********      Generic View    ***********
# path("gene/<int:id>/", GenericAPIView.as_view())......
# the problem is i  this url. when i want to fetch the special id that theme it not show the particular id data. 