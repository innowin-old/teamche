from django.shortcuts import render
from django.http import JsonResponse
from .models import Sms, Comment
from .serializers import (
    SmsSerializer,
    CommentSerializer,
    RateSerializer
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

    def get_queryset(self):
        queryset = Sms.objects.all()
        return queryset

    def get_serializer_class(self):
        return SmsSerializer

class CommentViewSet(ModelViewSet):
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset

    def get_serializer_class(self):
        return CommentSerializer


class RateViewSet(ModelViewSet):

    def get_queryset(self):
        queryset = Rate.objects.all()
        return queryset

    def get_serializer_class(self):
        return RateSerializer


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
