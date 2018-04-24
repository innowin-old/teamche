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


class ProductBrandSerializer(BaseSerializer):
    class Meta:
        model = ProductBrand
        fields = '__all__'


class ProductSerializer(BaseSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductPriceSerializer(BaseSerializer):
    class Meta:
        model = ProductPrice
        fields = '__all__'
