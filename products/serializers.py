from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer, ReadOnlyField

from .models import (
  ProductCategory,
  ProductBrand,
  Product,
  ProductPrice,
  ProductOffer
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
    product_related_category = ProductCategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'brand', 'made_in_iran', 'product_related_store', 'product_related_category', 'images', 'discount', 'price', 'active_flag', 'visibility_flag']
        extra_kwargs = {
          'product_related_user': { 'read_only': True }
        }

    def update(self, instance, validated_data):
        if validated_data.get('visibility_flag', None) != None:
            instance.visibility_flag = validated_data.get('visibility_flag', instance.visibility_flag)
            instance.save()
            return instance
        elif validated_data.get('active_flag', None) != None:
            instance.active_flag = validated_data.get('active_flag', instance.active_flag)
            instance.save()
            return instance
        else:
            if Product.objects.filter(related_parent_id=instance.id, active_flag=True).count() > 0:
                model = Product.objects.filter(related_parent_id=instance.id, active_flag=True)[0]
            else:
                model = Product()
            model.title = validated_data.get('title', instance.title)
            model.product_related_store = validated_data.get('product_related_store', instance.product_related_store)
            model.brand = validated_data.get('brand', instance.brand)
            model.product_related_category = validated_data.get('product_related_category', instance.product_related_category)
            model.product_related_user = validated_data.get('product_related_user', instance.product_related_user)
            model.made_in_iran = validated_data.get('made_in_iran', instance.made_in_iran)
            model.realted_parent = instance.id
            model.save()
            return model


class ProductAdminSerializer(BaseSerializer):
    images = ReadOnlyField()
    discount = ReadOnlyField()
    price = ReadOnlyField()
    product_related_category = ProductCategorySerializer()

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


class ProductOfferSerializer(BaseSerializer):
    class Meta:
        model = ProductOffer
        fields = '__all__'


class ProductOfferListSerializer(BaseSerializer):
    product_offer_related_product = ProductSerializer()

    class Meta:
        model = ProductOffer
        fields = '__all__'
