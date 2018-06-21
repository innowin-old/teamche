import base64

from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.crypto import get_random_string

from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response

from .models import (
    Sms,
    Comment,
    Rate,
    Favorite,
    Discount,
    Report,
    ViewModel,
    File,
    Slider,
    TopFilter
)
from .serializers import (
    SmsSerializer,
    CommentSerializer,
    CommentListSerializer,
    RateSerializer,
    FavoriteSerializer,
    FavoriteListSerializer,
    DiscountSerializer,
    ViewModelSerializer,
    ReportSerializer,
    FileSerializer,
    SliderSerializer,
    TopFilterSerializer
)
from users.models import User
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import jwt, json
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler


class BaseViewSet(ModelViewSet):
    def destroy(self, request, *args, **kwargs):
        """class DynamicDeleteSerializer(ModelSerializer, BaseSerializer):
            class Meta:
                model = self.get_serializer_class().Meta.model
                fields = []

            def validate(self, attrs):
                if self.instance.delete_flag:
                    raise ValidationError('Ths selected object does not exist or already deleted.')
                return attrs"""

        try:
            instance = self.get_object()
            # serializer = DynamicDeleteSerializer(instance, request.data)
            # serializer.is_valid(raise_exception=True)
            instance.delete_flag = True
            instance.save()
            # return Response({status: "SUCCESS"}, status=status.HTTP_200_OK)
            response = HttpResponse(json.dumps({'message': 'record deleted.'}),
                content_type='application/json')
            response.status_code = 200
            return response
        except Exception as e:
            if type(e) is ValidationError:
                raise e

        return Response({
            "errors": [{
                "status": 1,
                "key": "non_field_errors",
                "detail": "The selected object does not exist or already deleted."
            }]
        })


class SmsViewSet(BaseViewSet):
    permission_classes = [AllowAny]
    filter_fields = ['phone_number', 'code']

    def get_queryset(self):
        queryset = Sms.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return SmsSerializer

class CommentViewSet(BaseViewSet):
    permission_classes = [AllowAny]
    filter_fields = ['text', 'comment_related_parent', 'is_new', 'active_flag']

    def get_queryset(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            queryset = Comment.objects.filter(delete_flag=False)
        else:
            queryset = Comment.objects.filter(delete_flag=False, active_flag=True)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CommentListSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(comment_related_user=self.request.user)

    @list_route(methods=['get'])
    def create_confirmation(self, request):
        instances = Comment.objects.filter(related_parent=None, active_flag=False, delete_flag=False, is_new=True)
        serializer = CommentListSerializer(instances, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def update_confirmation(self, request):
        instances = Comment.objects.exclude(related_parent=None).filter(active_flag=False, delete_flag=False)
        serializer = CommentListSerializer(instances, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def accept(self, request, pk=None):
        instance = self.get_object()
        if instance.related_parent != None:
            instance.delete_flag = True
            instance.save()
            update_instance = instance.related_parent
            update_instance.text = instance.text
            update_instance.active_flag = True
            update_instance.save()
            serializer = CommentSerializer(update_instance)
            return Response(serializer.data)
        instance.active_flag = True
        instance.save()
        serializer = CommentSerializer(instance)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def deny(self, request, pk=None):
        instance = self.get_object()
        instance.delete_flag = True
        instance.save()


class RateViewSet(BaseViewSet):
    filter_fields = ['title', 'value', 'rate_related_parent']

    def get_queryset(self):
        queryset = Rate.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return RateSerializer

    def perform_create(self, serializer):
        serializer.save(rate_related_user=self.request.user)


class FavoriteViewSet(BaseViewSet):
    filter_fields = ['favorite_related_parent', 'favorite_related_user']

    def get_queryset(self):
        queryset = Favorite.objects.filter(delete_flag=False, favorite_related_parent__delete_flag=False, favorite_related_parent__active_flag=True)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return FavoriteListSerializer
        return FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(favorite_related_user=self.request.user)


class DiscountViewSet(BaseViewSet):
    filter_fields = ['discount_value', 'discount_related_parent']

    def get_queryset(self):
        queryset = Discount.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return DiscountSerializer

    def perform_create(self, serializer):
        serializer.save(discount_related_user=self.request.user)


class ViewModelViewSet(BaseViewSet):
    filter_fields = ['view_model_related_parent', 'view_model_related_user']

    def get_queryset(self):
        queryset = ViewModel.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return ViewModelSerializer

    def perform_create(self, serializer):
        serializer.save(view_model_related_user=self.request.user)


class ReportViewSet(BaseViewSet):
    filter_fields = ['report_text', 'report_related_parent']

    def get_queryset(self):
        queryset = Report.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return ReportSerializer

    def perform_create(self, serializer):
        serializer.save(report_related_user=self.request.user)


class FileViewSet(BaseViewSet):
    filter_fields = ['file_related_parent', 'file_related_user']

    def get_queryset(self):
        queryset = File.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return FileSerializer

    def perform_create(self, serializer):
        if self.request and self.request.user and self.request.user.is_superuser:
          serializer.save(file_related_user=self.request.user)
        else:
          serializer.save(file_related_user=self.request.user, active_flag=False, is_new=True)

    @list_route(methods=['post'])
    def upload_base64(self, request):
        # data = ContentFile(base64.b64decode(request.POST.get("file_path", "")), name='temp.' + ext) # You can save this as file instance.

        format, imgstr = request.POST.get("file_path", "").split(';base64,')
        ext = format.split('/')[-1]

        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext) # You can save this as file instance.

        file_instance = File(
          file_related_parent_id=request.POST.get("file_related_parent", None),
          file_related_user=request.user,
          file_path=data
        )
        file_instance.save()

        return Response({'status': 'SUCCESS'})

    @list_route(methods=['get'])
    def create_confirmation(self, request):
        queryset = File.objects.filter(is_new=True, active_flag=False, delete_flag=False)
        serializer = FileSerializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def accept(self, request, pk=None):
        instance = self.get_object()
        instance.acitve_flag = True
        instance.is_new = False
        instance.save()
        serializer = FileSerializer(instance)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def deny(self, request, pk=None):
        instance = self.get_object()
        instance.is_new = False
        instance.save()
        serializer = FileSerializer(instance)
        return Response(serializer.data)


class SliderViewSet(BaseViewSet):
    filter_fields = ['title', 'link']

    def get_queryset(self):
        queryset = Slider.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return SliderSerializer


class TopFilterViewSet(BaseViewSet):
    filter_fields = ['title', 'link', 'order']

    def get_queryset(self):
        queryset = TopFilter.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return TopFilterSerializer


@csrf_exempt
def login(request):
    try :
        if Sms.objects.filter(phone_number=request.POST['phone_number'], delete_flag=False).count() == 0:
            sms = Sms.objects.create(
              phone_number=request.POST['phone_number'],
              code='1234'
            )
        return JsonResponse({'status': 'SUCCESS'})
    except Exception as e :
        print(e)
        return JsonResponse({'status': 'FAILED'})


@csrf_exempt
def code_verify(request):
    try:
        if Sms.objects.filter(phone_number=request.POST.get('phone_number', ''), code=request.POST.get('code', ''), delete_flag=False).count() >= 1:
            sms = Sms.objects.filter(phone_number=request.POST.get('phone_number', ''), code=request.POST.get('code', ''), delete_flag=False)[0]
            sms.delete_flag = True
            if User.objects.filter(username=sms.phone_number, delete_flag=False, active_flag=True).count() > 0:
                user = User.objects.filter(username=sms.phone_number, delete_flag=False, active_flag=True)[0]
            elif User.objects.filter(username=sms.phone_number, delete_flag=True).count() > 0:
                old_user = User.objects.filter(username=sms.phone_number, delete_flag=True)[0]
                old_user.username = sms.phone_number + get_random_string(length=32)
                old_user.save()
                user = User.objects.create(username=sms.phone_number, password='!', delete_flag=False, active_flag=True)
            else:
                user = User.objects.create(username=sms.phone_number, password='!', delete_flag=False, active_flag=True)
            payload = jwt_payload_handler(user)
            encoded_token = jwt_encode_handler(payload)
            sms.save()
            return JsonResponse({'status': 'SUCCESS', 'token': str(encoded_token)})
        return JsonResponse({'status': 'FAILED'})
    except Exception as e:
        return JsonResponse({'status': str(e)})

@csrf_exempt
def code_decode(request):
    try:
        payload = jwt.decode(request.POST.get('token', ''), 'SECRET')
    except Exception as e:
        return JsonResponse({'status': e})
