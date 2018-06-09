import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from rest_framework.serializers import ModelSerializer, CharField, SerializerMethodField, ReadOnlyField
from .models import (
        Base,
        Sms,
        Comment,
        Rate,
        Favorite,
        Discount,
        ViewModel,
        Report,
        File,
        Slider,
        TopFilter
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

    def update(self, instance, validated_data):
        if validated_data.get('active_flag', None) != None:
            instance.is_new = False
            instance.save()
            return instance


class RateSerializer(BaseSerializer):
    class Meta:
        model = Rate
        fields = '__all__'
        extra_kwargs = {
          'rate_related_user': { 'read_only': True }
        }

    def create(self, validated_data):
        if Rate.objects.filter(rate_related_parent=validated_data.get('rate_related_parent', None), rate_related_user=validated_data.get('rate_related_user', None), title=validated_data.get('title', None)).count() > 0:
            raise ValueError('This user rated before')
        instance = Rate.objects.create(**validated_data)
        parent_instance = instance.rate.rate_related_parent
        rates = Rate.objects.filter(rate_related_parent=instance.rate_related_parent, delete_flag=False)
        sum = 0
        for rate in rates:
            sum += rate.value
        parent_instance.rate_average = sum / rates.count()
        parent_instance.save()
        return instance


class StoreDetailSerializer(BaseSerializer):
    images = ReadOnlyField()

    class Meta:
        model = Store
        fields = '__all__'


class FavoriteListSerializer(BaseSerializer):
    favorite_related_parent = SerializerMethodField()
    favorite_related_user = UserDetailSerializer()

    class Meta:
        model = Favorite
        fields = '__all__'

    def get_favorite_related_parent(self, obj):
        if Store.objects.filter(pk=obj.favorite_related_parent_id).count() > 0:
            store = Store.objects.get(pk=obj.favorite_related_parent_id)
            serializer = StoreDetailSerializer(store)
            return serializer.data
        else:
            instance = Base.objects.filter(pk=obj.favorite_related_parent_id)[0]
            serializer = BaseSerializer(instance)
            return serializer.data


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


class ViewModelSerializer(BaseSerializer):
    class Meta:
        model = ViewModel
        fields = '__all__'
        extra_kwargs = {
          'view_model_related_user': { 'read_only': True }
        }


class ReportSerializer(BaseSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        extra_kwargs = {
          'report_related_user': { 'read_only': True }
        }

class FileSerializer(BaseSerializer):
    file_link = ReadOnlyField()
    file_string = CharField(write_only=True)

    class Meta:
        model = File
        fields = '__all__'
        extra_kwargs = {
          'file_related_user': { 'read_only': True },
          'file_link': { 'read_only': True },
          'file_path': { 'read_only': True },
          'file_string': { 'write_only': True }
        }

    def create(self, validated_data):
        data = validated_data.pop('file_string')
        request = self.context.get("request")

        if data != '':
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            print(ext)
            validated_data['file_path'] = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
            if ext == 'mp4' or ext == 'avi' or ext == 'webm':
                validated_data['file_path'] = compress_video(validated_data['file_path'])

        file_obj = File.objects.create(**validated_data)
        return file_obj


class SliderSerializer(BaseSerializer):
    file_string = CharField(write_only=True)
    image = ReadOnlyField()

    class Meta:
        model = Slider
        fields = '__all__'

    def create(self, validated_data):
        try:
            data = validated_data.pop('file_string')
            request = self.context.get("request")

            if data != '':
                format, imgstr = data.split(';base64,')
                ext = format.split('/')[-1]
                print(ext)
                validated_data['file_path'] = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                if ext == 'mp4' or ext == 'avi' or ext == 'webm':
                    validated_data['file_path'] = compress_video(validated_data['file_path'])

            slider_instance = Slider.objects.create(title=validated_data.get('title', None), link=validated_data.get('link', None))

            file_obj = File.objects.create(file_related_parent_id=slider_instance.id, file_related_user_id=request.user.id, file_path=validated_data.get('file_path', None))
            return slider_instance
        except Exception as e:
            print(e)


class TopFilterSerializer(BaseSerializer):
    class Meta:
        model = TopFilter
        fields = '__all__'
