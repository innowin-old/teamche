from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer, ReadOnlyField
from .models import (
    StoreCategory,
    Store,
    StoreVisit
)
from users.models import User


class UserDetailSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name']


class StoreCategorySerializer(BaseSerializer):
    image = ReadOnlyField()

    class Meta:
        model = StoreCategory
        fields = '__all__'


class StoreDetailSerializer(BaseSerializer):
    store_related_category = StoreCategorySerializer()
    images = ReadOnlyField()
    store_related_owner = UserDetailSerializer()
    store_related_user = UserDetailSerializer()

    class Meta:
        model = Store
        fields = '__all__'


class StoreAdminSerializer(BaseSerializer):
    image = ReadOnlyField()
    bookmark = ReadOnlyField()

    class Meta:
        model = Store
        fields = '__all__'
        extra_kwargs = {
          'store_related_user': { 'read_only': True }
        }

    def update(self, instance, validated_data):
        if validated_data.get('visibility_flag', None) != None:
            instance.visibility_flag = validated_data.get('visibility_flag', None)
        elif validated_data.get('active_flag', None) != None:
            instance.active_flag = validated_data.get('active_flag', None)
            instance.is_new = False
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.store_related_category = validated_data.get('store_related_category', instance.store_related_category)
        instance.store_related_owner = validated_data.get('store_related_owner', instance.store_related_owner)
        instance.store_related_user = validated_data.get('store_related_user', instance.store_related_user)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get('longitude', instance.longitude)
        instance.address = validated_data.get('address', instance.address)
        instance.related_logo = validated_data.get('related_logo', instance.related_logo)
        instance.save()
        return instance


class StoreSerializer(BaseSerializer):
    image = ReadOnlyField()
    bookmark = ReadOnlyField()

    class Meta:
        model = Store
        fields = '__all__'
        extra_kwargs = {
          'store_related_user': { 'read_only': True }
        }

    def update(self, instance, validated_data):
        if validated_data.get('visibility_flag', None) != None:
            instance.visibility_flag = validated_data.get('visibility_flag', None)
            instance.save()
            return instance
        elif validated_data.get('active_flag', None) != None:
            instance.active_flag = validated_data.get('active_flag', None)
            instance.is_new = False
            instance.save()
            return instance
        else:
            if Store.objects.filter(related_parent_id=instance.id, delete_flag=False).count() > 0:
                model = Store.objects.filter(related_parent_id=instance.id, delete_flag=False)[0]
            else:
                model = Store()
            model.title = validated_data.get('title', instance.title)
            model.description = validated_data.get('description', instance.description)
            model.store_related_category = validated_data.get('store_related_category', instance.store_related_category)
            model.store_related_owner = validated_data.get('store_related_owner', instance.store_related_owner)
            model.store_related_user = validated_data.get('store_related_user', instance.store_related_user)
            model.phone_number = validated_data.get('phone_number', instance.phone_number)
            model.latitude = validated_data.get('latitude', instance.latitude)
            model.longitude = validated_data.get('longitude', instance.longitude)
            model.address = validated_data.get('address', instance.address)
            model.related_logo = validated_data.get('related_logo', instance.related_logo)
            model.related_parent_id = instance.id
            model.save()
            return model


class StoreVisitDetailSerializer(BaseSerializer):
    store_visit_related_user = UserDetailSerializer()

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
