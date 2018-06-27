from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer, ReadOnlyField, SerializerMethodField

from .models import (
  ProductCategory,
  ProductBrand,
  Product,
  ProductPrice,
  ProductOffer
)

from stores.models import Store, StoreCategory

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


class StoreCategorySerializer(BaseSerializer):
    image = ReadOnlyField()

    class Meta:
        model = StoreCategory
        fields = '__all__'


class StoreSerializer(BaseSerializer):
    store_related_category = StoreCategorySerializer()
    class Meta:
        model = Store
        fields = ['id', 'title', 'latitude', 'longitude', 'store_related_category', 'visibility_flag']


class ProductListSerializer(BaseSerializer):
    images = ReadOnlyField()
    discount = ReadOnlyField()
    price = ReadOnlyField()
    product_related_category = ProductCategorySerializer()
    product_related_store = StoreSerializer()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'brand', 'made_in_iran', 'product_related_store', 'product_related_category', 'images', 'discount', 'price', 'active_flag', 'visibility_flag']


class ProductSerializer(BaseSerializer):
    images = ReadOnlyField()
    discount = ReadOnlyField()
    price = ReadOnlyField()

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
            if instance.related_parent != None:
                model = Product.objects.filter(id=instance.id)
            elif Product.objects.filter(related_parent_id=instance.id, delete_flag=False).count() > 0:
                model = Product.objects.filter(related_parent_id=instance.id, delete_flag=False)[0]
            else:
                model = Product()
            model.title = validated_data.get('title', instance.title)
            model.description = validated_data.get('description', instance.description)
            model.product_related_store = validated_data.get('product_related_store', instance.product_related_store)
            model.brand = validated_data.get('brand', instance.brand)
            model.product_related_category = validated_data.get('product_related_category', instance.product_related_category)
            model.product_related_user = validated_data.get('product_related_user', instance.product_related_user)
            model.made_in_iran = validated_data.get('made_in_iran', instance.made_in_iran)
            model.related_parent_id = instance.id
            model.save()
            # Set new price
            """ if instance.price != validated_data.get('price', instance.price):
                price_instance = ProductPrice()
                if instance.related_parent != None:
                    price_instance.product_price_related_product = instance.related_parent
                else:
                    price_instance.product_price_related_product = instance
                price_instance.amount = validated_data.get('price', instance.price)
                price_instance.save() """

            return model


class ProductAdminListSerializer(BaseSerializer):
    images = ReadOnlyField()
    discount = ReadOnlyField()
    price = ReadOnlyField()
    product_related_category = ProductCategorySerializer()
    product_related_store = StoreSerializer()
    related_parent = SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_related_parent(self, obj):
        if Product.objects.filter(id=obj.related_parent_id).count() > 0:
            instance = Product.objects.filter(id=obj.related_parent_id)[0]
            serializer = ProductListSerializer(instance)
            return serializer.data
        return None


class ProductAdminSerializer(BaseSerializer):
    images = ReadOnlyField()
    discount = ReadOnlyField()
    price = ReadOnlyField()

    class Meta:
        model = Product
        fields = '__all__'
        extra_kwargs = {
          'product_related_user': { 'read_only': True }
        }

    def update(self, instance, validated_data):
        if validated_data.get('visibility_flag', None) != None:
            instance.visibility_flag = validated_data.get('visibility_flag', instance.visibility_flag)
        elif validated_data.get('active_flag', None) != None:
            instance.active_flag = validated_data.get('active_flag', instance.active_flag)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.product_related_store = validated_data.get('product_related_store', instance.product_related_store)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.product_related_category = validated_data.get('product_related_category', instance.product_related_category)
        instance.product_related_user = validated_data.get('product_related_user', instance.product_related_user)
        instance.made_in_iran = validated_data.get('made_in_iran', instance.made_in_iran)
        instance.save()

        print(validated_data)

        if instance.price != validated_data.get('price', instance.price):
            print("OK")
            price_instance = ProductPrice()
            if instance.related_parent != None:
                price_instance.product_price_related_product = instance.related_parent
            else:
                price_instance.product_price_related_product = instance
            price_instance.amount = validated_data.get('price', instance.price)
            price_instance.save()

        if instance.discount.value != validated_data.get('discount', instance.discount):
            discount_instance = Discount()
            if instance.related_parent != None:
                discount_instance.discount_related_parent = instance.related_parent
            else:
                discount_instance.discount_related_parent = instance
            discount_instance.discount_value = validated_data.get('discount', instance.discount.value)
            discount_instance.save()

        return instance


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
    product_offer_related_product = ProductListSerializer()

    class Meta:
        model = ProductOffer
        fields = '__all__'
