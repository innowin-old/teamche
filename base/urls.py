from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import SimpleRouter

from .views import (
    SmsViewSet,
    CommentViewSet,
    RateViewSet
)

router = SimpleRouter()
router.register(r'comments', CommentViewSet, 'base-comments')
router.register(r'sms', SmsViewSet, 'base-sms')
router.register(r'rates', RateViewSet, 'base-rates')

urlpatterns = [
    url(r'^', include(router.urls))
]
