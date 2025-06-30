from rest_framework import serializers
from .models import News

class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
