from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from base.views import BaseViewSet

from .models import (
  Post
)

from .serializers import (
  PostSerializer,
  PostAdminSerializer
)


class PostViewSet(BaseViewSet):
    filter_fields = ['id', 'title', 'text', 'created_time']

    def get_queryset(self):
        queryset = Post.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return PostAdminSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(post_related_user=self.request.user, active_flag=True)

    @list_route(methods=['get'])
    def create_confirmation(self, request):
        instances = Post.objects.filter(related_parent=None, active_flag=False, delete_flag=False)
        serializer = PostSerializer(instances, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def update_confirmation(self, request):
        instances = Post.objects.exclude(related_parent=None).filter(active_flag=False, delete_flag=False)
        serializer = PostSerializer(instances, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def accept(self, request, pk=None):
        instance = self.get_object()
        if instance.related_parent != None:
            instance.delete_flag = True
            instance.save()
            update_instance = instance.related_parent
            update_instance.title = instance.title
            update_instance.text = instance.text
            update_instance.save()
        instance.active_flag = True
        instance.save()
        serializer = PostSerializer(instacne)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def deny(self, request, pk=None):
        instance = self.get_object()
        instance.delete_flag = True
        instance.save()
        serializer = PostSerializer(instance)
        return Response(serializer.data)
