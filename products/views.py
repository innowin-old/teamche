from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response
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
    filter_fields = ['title', 'product_category_related_parent', 'product_category_related_user']
    ordering_fields = '__all__'

    def queryset(self):
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
        if self.request.user.is_superuser:
            return ProductBrandAdminSerializer
        return ProductBrandSerializer

    def perform_create(self, serializer):
        serializer.save(product_brand_related_user=self.request.user)


class ProductViewSet(ModelViewSet):
    filter_fields = ['title', 'product_related_parent', 'brand', 'product_related_category', 'product_realted_user', 'made_in_iran']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = Product.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return ProductAdminSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        serializer.save(product_related_user=self.request.user)


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
