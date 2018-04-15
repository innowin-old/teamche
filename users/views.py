from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import (
    User
  )

from .serializers import (
    UserSerializer
  )


class UserViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset =  User.objects.all()
        return queryset

    def get_serializer_class(self):
        return UserSerializer
