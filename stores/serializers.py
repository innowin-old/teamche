from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer, ReadOnlyField
from .models import (
    StoreCategory,
    Store,
    StoreVisit
)

class StoreCategorySerializer(BaseSerializer):
    image = ReadOnlyField()

    class Meta:
        model = StoreCategory
        fields = '__all__'


class StoreDetailSerializer(BaseSerializer):
    store_related_category = StoreCategorySerializer()
    images = ReadOnlyField()

    class Meta:
        model = Store
        fields = '__all__'


class StoreSerializer(BaseSerializer):
    class Meta:
        model = Store
        fields = '__all__'
        extra_kwargs = {
          'store_related_user': { 'read_only': True }
        }


class StoreVisitDetailSerializer(BaseSerializer):
    store_visit_related_store = StoreDetailSerializer()

    class Meta:
        model = StoreVisit
        fields = '__all__'


class StoreVisitSerializer(BaseSerializer):
    class Meta:
        model = StoreVisit
        fields = '__all__'
        extra_kwargs = {
          'store_visit_related_user': { 'read_only': True }
        }
