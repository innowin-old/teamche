from rest_framework.serializers import ModelSerializer, CharField
from .models import (
        Base,
        Sms,
        Comment,
        Rate,
        Favorite,
        Discount,
        Report
    )
from stores.models import Store
from users.models import User


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


class UserDetailSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name']


class CommentListSerializer(BaseSerializer):
    comment_related_user = UserDetailSerializer()

    class Meta:
        model = Comment
        fields = '__all__'


class CommentSerializer(BaseSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {
          'comment_related_user': { 'read_only': True }
        }


class RateSerializer(BaseSerializer):
    class Meta:
        model = Rate
        fields = '__all__'
        extra_kwargs = {
          'rate_related_user': { 'read_only': True }
        }


class StoreDetailSerializer(BaseSerializer):
    class Meta:
        model = Base
        fields = '__all__'


class FavoriteListSerializer(BaseSerializer):
    favorite_related_parent = StoreDetailSerializer()

    class Meta:
        model = Favorite
        fields = '__all__'


class FavoriteSerializer(BaseSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'
        extra_kwargs = {
          'favorite_related_user': { 'read_only': True }
        }


class DiscountSerializer(BaseSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
        extra_kwargs = {
          'discount_related_user': { 'read_only': True }
        }


class ReportSerializer(BaseSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        extra_kwargs = {
          'report_related_user': { 'read_only': True }
        }
