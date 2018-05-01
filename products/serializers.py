from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer, ReadOnlyField

from .models import (
  ProductCategory,
  ProductBrand,
  Product,
  ProductPrice
)


class ProductCategorySerializer(BaseSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'title', 'product_category_related_parent', 'product_category_related_store']
        extra_kwargs = {
          'product_category_related_user': { 'read_only': True }
        }


class ProductCategoryAdminSerializer(BaseSerializer):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class ProductBrandSerializer(BaseSerializer):
    class Meta:
        model = ProductBrand
        fields = ['id', 'title', 'product_brand_related_store']
        extra_kwargs = {
          'product_brand_related_user': { 'read_only': True }
        }


class ProductBrandAdminSerializer(BaseSerializer):
    class Meta:
        model = ProductBrand
        fields = '__all__'


class ProductSerializer(BaseSerializer):
    images = ReadOnlyField()
    discount = ReadOnlyField()
    price = ReadOnlyField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'brand', 'made_in_iran', 'product_related_store', 'product_related_category', 'images', 'discount', 'price']
        extra_kwargs = {
          'product_related_user': { 'read_only': True }
        }


class ProductAdminSerializer(BaseSerializer):
    images = ReadOnlyField()
    discount = ReadOnlyField()
    price = ReadOnlyField()

    class Meta:
        model = Product
        fields = '__all__'


class ProductPriceSerializer(BaseSerializer):
    class Meta:
        model = ProductPrice
        fields = ['id', 'product_price_related_product', 'amount']
        extra_kwargs = {
          'product_price_related_user': { 'read_only': True }
        }


class ProductPriceAdminSerializer(BaseSerializer):
    class Meta:
        model = ProductPrice
        fields = '__all__'
