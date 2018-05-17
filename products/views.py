from django.shortcuts import render
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from .models import (
  ProductCategory,
  ProductBrand,
  Product,
  ProductPrice
)

from .serializers import (
  ProductCategorySerializer,
  ProductCategoryAdminSerializer,
  ProductBrandSerializer,
  ProductBrandAdminSerializer,
  ProductSerializer,
  ProductAdminSerializer,
  ProductPriceSerializer,
  ProductPriceAdminSerializer
)


class ProductCategoryViewSet(ModelViewSet):
    filter_fields = ['title', 'product_category_related_parent', 'product_category_related_user', 'product_category_related_store']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = ProductCategory.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return ProductCategoryAdminSerializer
        return ProductCategorySerializer

    def perform_create(self, serializer):
        serializer.save(product_category_related_user=self.request.user)


class ProductBrandViewSet(ModelViewSet):
    filter_fields = ['title', 'product_brand_related_store', 'product_brand_related_user']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = ProductBrand.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return ProductBrandAdminSerializer
        return ProductBrandSerializer

    def perform_create(self, serializer):
        serializer.save(product_brand_related_user=self.request.user)


class ProductViewSet(ModelViewSet):
    filter_fields = ['id', 'title', 'product_related_store', 'brand', 'product_related_category', 'product_related_user', 'made_in_iran']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = Product.objects.filter(Q(delete_flag=False) | Q(active_flag=True) | Q(active_flag=False, product_related_user=self.request.user))

        related_parent = self.request.query_params.get('related_parent', None)
        if related_parent is not None:
            if related_parent == 'null':
                queryset = queryset.filter(related_parent=None)
            else:
                queryset = queryset.filter(related_parent_id=related_parent)

        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return ProductAdminSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        data = self.request.data

        serializer.save(product_related_user=self.request.user)
        if ProductBrand.objects.filter(title=data.get('brand', ''), product_brand_related_store_id=data.get('product_related_store', ''), product_brand_related_user=self.request.user).count() == 0:
            instance = ProductBrand.objects.create(title=data.get('brand', ''), product_brand_related_store_id=data.get('product_related_store', ''), product_brand_related_user=self.request.user)

    @detail_route(methods=['post'])
    def accept_update(self, request, pk=None):
        update_instance = self.get_object()
        if update_instance.delete_falg == False:
            instance = update_instance.related_parent
            instance = update_instance
            instance.related_parent = None
            instance.active_flag = True
            instance.save()
            update_instance.delete_falg = True
            update_instance.save()
            serializer = ProductSerializer(instance)
            return serializer.data
        else:
            return Response({'status': 'Update request not found'})

    @detail_route(methods=['post'])
    def deny_update(self, request, pk=None):
        update_instance = self.get_object()
        update_instance.delete_flag = True
        update_instance.save()
        return Response({'status': 'Update request denied'})


class ProductPriceViewSet(ModelViewSet):
    filter_fields = ['product_price_related_product', 'amount', 'product_price_related_user']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = ProductPrice.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return ProductPriceAdminSerializer
        return ProductPriceSerializer

    def perform_create(self, serializer):
        serializer.save(product_price_related_user=self.request.user)
