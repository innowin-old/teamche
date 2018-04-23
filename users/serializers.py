from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer

from .models import (
    User,
    UpgradeRequest
  )

class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UpgradeRequestSerializer(BaseSerializer):
    class Meta:
        model = UpgradeRequest
        fields = '__all__'
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
