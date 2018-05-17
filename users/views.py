from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response
from .models import (
    User,
    UpgradeRequest,
    FCMToken
  )

from .serializers import (
    UserSerializer,
    UserAdminSerializer,
    UpgradeRequestSerializer,
    UpgradeRequestAdminSerializer,
    UpgradeRequestUserSerializer,
    FCMTokenSerializer,
    FCMTokenAdminSerializer
  )


class UserViewSet(ModelViewSet):
    filter_fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender', 'type']
    search_fields = ['username', 'first_name', 'last_name', 'email']

    def get_queryset(self):
        queryset =  User.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return UserAdminSerializer
        return UserSerializer

    @list_route(methods=['get'])
    def get_profile(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response(e)


class UpgradeRequestViewSet(ModelViewSet):
    filter_fields = ['upgrade_request_related_user', 'first_name', 'last_name', 'gender']

    def get_queryset(self):
        queryset = UpgradeRequest.objects.filter(delete_flag=False, active_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return UpgradeRequestAdminSerializer
        return UpgradeRequestSerializer

    def perform_create(self, serializer):
        serializer.save(upgrade_request_related_user=self.request.user)


class FCMTokenViewSet(ModelViewSet):
    filter_fields = ['fcm_token_related_user', 'token']

    def get_queryset(self):
        queryset = FCMToken.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return FCMTokenAdminSerializer
        return FCMTokenSerializer

    def perform_create(self, serializer):
        serializer.save(fcm_token_related_user=self.request.user)
