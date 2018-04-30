from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response

from .models import (
  Post
)

from .serializers import (
  PostSerializer,
  PostAdminSerializer
)


class PostViewSet(ModelViewSet):
    filter_fields = ['id', 'title', 'text', 'created_time']

    def get_queryset(self):
        queryset = Post.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return PostAdminSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(post_related_user=self.request.user)
