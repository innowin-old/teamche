from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import (
    StoreCategory,
    Store,
    StoreVisit
)

from .serializers import (
    StoreCategorySerializer,
    StoreSerializer,
    StoreDetailSerializer,
    StoreVisitSerializer,
    StoreVisitDetailSerializer
)


class StoreCategoryViewSet(ModelViewSet):
    filter_fields = ['title']

    def get_queryset(self):
        queryset = StoreCategory.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return StoreCategorySerializer


class StoreViewSet(ModelViewSet):
    filter_fields = ['title', 'description', 'phone_number', 'latitude', 'longitude', 'store_related_category', 'store_related_owner']

    def get_queryset(self):
        queryset = Store.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return StoreDetailSerializer
        return StoreSerializer

    def perform_create(self, serializer):
        serializer.save(store_related_user=self.request.user)


class StoreVisitViewSet(ModelViewSet):
    filter_fields = ['store_visit_related_store', 'store_visit_related_user', 'active_flag', 'delete_flag']

    def get_queryset(self):
        queryset = StoreVisit.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return StoreVisitDetailSerializer
        return StoreVisitSerializer

    def perform_create(self, serializer):
        serializer.save(store_visit_related_user=self.request.user, active_flag=False)
