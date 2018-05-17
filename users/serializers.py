from rest_framework.serializers import ModelSerializer, ReadOnlyField
from base.serializers import BaseSerializer

from .models import (
    User,
    UpgradeRequest,
    FCMToken
  )

class UserAdminSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = [
          'id',
          'username',
          'first_name',
          'last_name',
          'email',
          'gender',
          'type'
        ]
        extra_kwargs = {
          'type': { 'read_only': True }
        }


class UpgradeRequestAdminSerializer(BaseSerializer):
    member_type = ReadOnlyField()

    class Meta:
        model = UpgradeRequest
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.active_flag = validated_data.get('active_flag', instance.active_flag)
        instance.delete_flag = validated_data.get('delete_flag', instance.delete_flag)
        if validated_data.get('active_flag', None) != None:
            user = User.objects.filter(id=instance.upgrade_request_related_user_id)[0]
            user.type = instance.type
            user.save()
        instance.save()
        return instance


class UpgradeRequestSerializer(BaseSerializer):
    member_type = ReadOnlyField()

    class Meta:
        model = UpgradeRequest
        fields = ['id', 'first_name', 'last_name', 'gender', 'active_flag', 'type', 'member_type']
        extra_kwargs = {
          'upgrade_request_related_user': { 'read_only': True }
        }


class UpgradeRequestUserSerializer(BaseSerializer):
    class Meta:
        model = UpgradeRequest
        fields = '__all__'
        extra_kwargs = {
          'upgrade_request_related_user': { 'read_only': True },
          'active_flag': { 'read_only': True },
          'updated_time': { 'read_only': True }
        }


class FCMTokenSerializer(BaseSerializer):
    class Meta:
        model = FCMToken
        fields = '__all__'
        extra_kwargs = {
          'fcm_token_related_user': { 'read_only': True },
          'active_flag': { 'read_only': True },
          'update_time': { 'read_only': True }
        }
