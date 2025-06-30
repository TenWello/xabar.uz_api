from django.urls import path
from .views import LatestNewsList

urlpatterns = [
    path('xabar-news/', LatestNewsList.as_view(), name='xabar-news'),
]