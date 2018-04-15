from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import (
    StoreCategory,
    Store
)

from .serializers import (
    StoreCategorySerializer,
    StoreSerializer
)


class StoreCategoryViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = StoreCategory.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return StoreCategorySerializer


class StoreViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Store.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return StoreSerializer
