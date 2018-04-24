from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer

from .models import (
  ProductCategory,
  ProductBrand,
  Product,
  ProductPrice
)


class ProductCategorySerializer(BaseSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'
        extra_kwargs = {
          'product_category_related_user': { 'read_only': True }
        }


class ProductBrandSerializer(BaseSerializer):
    class Meta:
        model = ProductBrand
        fields = '__all__'
        extra_kwargs = {
          'product_brand_related_user': { 'read_only': True }
        }


class ProductSerializer(BaseSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
          'product_related_user': { 'read_only': True }
        }


class ProductPriceSerializer(BaseSerializer):
    class Meta:
        model = ProductPrice
        fields = '__all__'
        extra_kwargs = {
          'product_price_related_user': { 'read_only': True }
        }
