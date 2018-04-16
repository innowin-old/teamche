from rest_framework.serializers import ModelSerializer, CharField
from .models import (
        Base,
        Sms,
        Comment,
        Rate
    )


class BaseSerializer(ModelSerializer):
    class Meta:
        model = Base
        fields = '__all__'
        extra_kwargs = {
            'updated_time': {'read_only': True}
        }


class SmsSerializer(BaseSerializer):
    class Meta:
        model = Sms
        fields = '__all__'


class CommentSerializer(BaseSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class RateSerializer(BaseSerializer):
    class Meta:
        model = Rate
        fields = '__all__'
