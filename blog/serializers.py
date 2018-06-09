from rest_framework.serializers import ModelSerializer, ReadOnlyField
from base.serializers import BaseSerializer

from .models import (
  Post
)


class PostSerializer(BaseSerializer):
    image = ReadOnlyField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'text', 'image']
        extra_kwargs = {
          'post_related_user': { 'read_only': True }
        }


class PostAdminSerializer(BaseSerializer):
    image = ReadOnlyField()

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {
          'post_related_user': { 'read_only': True }
        }
