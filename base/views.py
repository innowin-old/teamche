from django.shortcuts import render
from django.http import JsonResponse
from .models import Sms, Comment, Rate, Favorite, Discount, Report
from .serializers import (
    SmsSerializer,
    CommentSerializer,
    CommentListSerializer,
    RateSerializer,
    FavoriteSerializer,
    FavoriteListSerializer,
    DiscountSerializer,
    ReportSerializer
)
from users.models import User
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import jwt, json
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_jwt.utils import jwt_payload_handler, jwt_encode_handler

class SmsViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    filter_fields = ['phone_number', 'code']

    def get_queryset(self):
        queryset = Sms.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return SmsSerializer

class CommentViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    filter_fields = ['text', 'comment_related_parent']

    def get_queryset(self):
        queryset = Comment.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return CommentListSerializer
        return CommentSerializer

    def perform_create(self, serializer):
        serializer.save(comment_related_user=self.request.user)


class RateViewSet(ModelViewSet):
    filter_fields = ['title', 'value', 'rate_related_parent']

    def get_queryset(self):
        queryset = Rate.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return RateSerializer

    def perform_create(self, serializer):
        serializer.save(rate_related_user=self.request.user)


class FavoriteViewSet(ModelViewSet):
    filter_fields = ['favorite_related_parent', 'favorite_related_user']

    def get_queryset(self):
        queryset = Favorite.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return FavoriteListSerializer
        return FavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(favorite_related_user=self.request.user)


class DiscountViewSet(ModelViewSet):
    filter_fields = ['discount_value', 'discount_related_parent']

    def get_queryset(self):
        queryset = Discount.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return DiscountSerializer

    def perform_create(self, serializer):
        serializer.save(discount_related_user=self.request.user)


class ReportViewSet(ModelViewSet):
    filter_fields = ['report_text', 'report_related_parent']

    def get_queryset(self):
        queryset = Report.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        return ReportSerializer

    def perform_create(self, serializer):
        serializer.save(report_related_user=self.request.user)


@csrf_exempt
def login(request):
    try :
        if Sms.objects.filter(phone_number=request.POST['phone_number'], delete_flag=False).count() == 0:
            sms = Sms.objects.create(
              phone_number=request.POST['phone_number'],
              code='1234'
            )
        return JsonResponse({'status': 'SUCCESS'})
    except :
        return JsonResponse({'status': 'FAILED'})


@csrf_exempt
def code_verify(request):
    try:
        if Sms.objects.filter(phone_number=request.POST.get('phone_number', ''), code=request.POST.get('code', ''), delete_flag=False).count() >= 1:
            sms = Sms.objects.get(phone_number=request.POST.get('phone_number', ''), code=request.POST.get('code', ''), delete_flag=False)
            sms.delete_flag = True
            if User.objects.filter(username=sms.phone_number).count() > 0:
                user = User.objects.filter(username=sms.phone_number)[0]
            else:
                user = User.objects.create(username=sms.phone_number, password='!')
            payload = jwt_payload_handler(user)
            encoded_token = jwt_encode_handler(payload)
            sms.save()
            return JsonResponse({'status': 'SUCCESS', 'token': str(encoded_token)})
        return JsonResponse({'status': 'FAILED'})
    except Exception as e:
        return JsonResponse({'status': e})

@csrf_exempt
def code_decode(request):
    try:
        payload = jwt.decode(request.POST.get('token', ''), 'SECRET')
    except Exception as e:
        return JsonResponse({'status': e})
