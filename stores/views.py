from django.shortcuts import render
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

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
    filter_fields = ['id', 'title', 'description', 'phone_number', 'latitude', 'longitude', 'store_related_category', 'store_related_owner', 'rate_average']
    ordering_fields = ['id', 'title', 'created_time']

    def get_queryset(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            queryset = Store.objects.filter(delete_flag=False).order_by('-pk')
        else:
            queryset = Store.objects.filter(Q(delete_flag=False, active_flag=True, visibility_flag=True) | Q(delete_flag=False, active_flag=False, store_related_user=self.request.user)).order_by('-pk')

        latitude__lte = self.request.query_params.get('latitude__lte', None)
        if latitude__lte is not None:
            queryset  = queryset.filter(latitude__lte=latitude__lte)

        latitude__gte = self.request.query_params.get('latitude__gte', None)
        if latitude__gte is not None:
            queryset = queryset.filter(latitude__gte=latitude__gte)

        longitude__lte = self.request.query_params.get('longitude__lte', None)
        if longitude__lte is not None:
            queryset = queryset.filter(longitude__lte=longitude__lte)

        longitude__gte = self.request.query_params.get('longitude__gte', None)
        if longitude__gte is not None:
            queryset = queryset.filter(longitude__gte=longitude__gte)

        related_parent = self.request.query_params.get('related_parent', None)
        if related_parent is not None:
            if related_parent == 'null':
                queryset = queryset.filter(related_parent=None)
            else:
                queryset = queryset.filter(related_parent_id=related_parent)

        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return StoreDetailSerializer
        return StoreSerializer

    def perform_create(self, serializer):
        serializer.save(store_related_user=self.request.user)

    @detail_route(methods=['post'])
    def accept_update(self, request, pk=None):
        update_instance = self.get_object()
        if update_instance.delete_flag == False:
            instance = update_instance.related_parent
            instance = update_instance
            instance.related_parent = None
            instance.active_flag = True
            instance.save()
            update_instance.delete_flag = True
            update_instance.save()
            serializer = StoreSerializer(instance)
            return Response(serializer.data)
        else:
            return Response({'status': 'Update Request Denied Before'})

    @detail_route(methods=['post'])
    def deny_update(self, request, pk=None):
        update_instance = self.get_object()
        update_instance.delete_falg = True
        update_instance.save()
        return Response({'status': 'Update Request Denied'})


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
