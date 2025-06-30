from rest_framework.generics import ListAPIView
from .models import News
from .serializers import NewsItemSerializer

class LatestNewsList(ListAPIView):
    queryset = News.objects.order_by('-published_at')[:20]
    serializer_class = NewsItemSerializer