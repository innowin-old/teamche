import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, ReadOnlyField
from .models import (
        Discount,
    )
from products.models import Product
from base.serializers import BaseSerializer


class DiscountSerializer(BaseSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
        extra_kwargs = {
          'discount_related_user': { 'read_only': True }
        }

    def create(self, validated_data):
        obj = Discount.objects.create(**validated_data)
        obj.save()
        if Product.objects.filter(id=obj.discount_related_parent_id).count() > 0:
            related_product_instance = Product.objects.filter(id=obj.discount_related_parent_id)[0]
            if Product.objects.filter(related_parent=obj.discount_related_parent, active_flag=True, delete_flag=False).count() == 0:
                product_instance = Product.objects.filter(id=obj.discount_related_parent_id)[0]
                product_update_instance = Product()
                product_update_instance.title = product_instance.title
                product_update_instance.description = product_instance.description
                product_update_instance.brand = product_instance.brand
                product_update_instance.product_related_store = product_instance.product_related_store
                product_update_instance.product_related_category = product_instance.product_related_category
                product_update_instance.related_parent = product_instance
                product_update_instance.product_related_user = related_product_instance.product_related_user
                product_update_instance.save()
        return obj
