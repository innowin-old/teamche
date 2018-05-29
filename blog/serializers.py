from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer

from .models import (
  Post
)


class PostSerializer(BaseSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'text']
        extra_kwargs = {
          'post_related_user': { 'read_only': True }
        }


class PostAdminSerializer(BaseSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
          'post_related_user': { 'read_only': True }
        }
