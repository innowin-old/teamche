from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer
from .models import StoreCategory, Store

class StoreCategorySerializer(BaseSerializer):
    class Meta:
        model = StoreCategory
        fields = '__all__'

class StoreSerializer(BaseSerializer):
    class Meta:
        model = Store
        fields = '__all__'
