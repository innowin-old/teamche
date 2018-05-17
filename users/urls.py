from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import SimpleRouter

from .views import (
    UserViewSet,
    UpgradeRequestViewSet,
    FCMTokenViewSet
  )

router = SimpleRouter()
router.register(r'upgrade-requests', UpgradeRequestViewSet, 'users-upgrade-requests')
router.register(r'fcm-tokens', FCMTokenViewSet, 'users-fcm-tokens')
router.register(r'', UserViewSet, 'users')

urlpatterns = [
    url(r'^', include(router.urls))
]
