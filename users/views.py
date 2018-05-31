from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response

from base.views import BaseViewSet

from .models import (
    User,
    UpgradeRequest,
    FCMToken
  )

from .serializers import (
    UserSerializer,
    UserAdminSerializer,
    UpgradeRequestSerializer,
    UpgradeRequestAdminSerializer,
    UpgradeRequestUserSerializer,
    FCMTokenSerializer,
    FCMTokenAdminSerializer
  )


class UserViewSet(ModelViewSet):
    filter_fields = ['id', 'username', 'first_name', 'last_name', 'email', 'gender', 'type']
    search_fields = ['username', 'first_name', 'last_name', 'email']

    def get_queryset(self):
        queryset =  User.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return UserAdminSerializer
        return UserSerializer

    @list_route(methods=['get'])
    def get_profile(self, request):
        try:
            user = User.objects.get(id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response(e)

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
            instance.is_active = False
            instance.save()
            # return Response({status: "SUCCESS"}, status=status.HTTP_200_OK)
            response = HttpResponse(json.dumps({'message': 'record deleted.'}), content_type='application/json')
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



class UpgradeRequestViewSet(BaseViewSet):
    filter_fields = ['upgrade_request_related_user', 'first_name', 'last_name', 'gender']

    def get_queryset(self):
        queryset = UpgradeRequest.objects.filter(delete_flag=False, active_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return UpgradeRequestAdminSerializer
        return UpgradeRequestSerializer

    def perform_create(self, serializer):
        serializer.save(upgrade_request_related_user=self.request.user)


class FCMTokenViewSet(BaseViewSet):
    filter_fields = ['fcm_token_related_user', 'token']

    def get_queryset(self):
        queryset = FCMToken.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return FCMTokenAdminSerializer
        return FCMTokenSerializer

    def perform_create(self, serializer):
        serializer.save(fcm_token_related_user=self.request.user)
