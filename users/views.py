from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response
from .models import (
    User
  )

from .serializers import (
    UserSerializer
  )


class UserViewSet(ModelViewSet):
    filter_fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'type']

    def get_queryset(self):
        queryset =  User.objects.all()
        return queryset

    def get_serializer_class(self):
        return UserSerializer

    @list_route(methods=['get'])
    def get_profile(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response(e)
