from rest_framework.serializers import ModelSerializer
from base.serializers import BaseSerializer

from .models import (
    User
  )

class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = '__all__'
