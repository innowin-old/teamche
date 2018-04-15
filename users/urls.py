from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import SimpleRouter

from .views import (
    UserViewSet
  )

router = SimpleRouter()
router.register(r'', UserViewSet, 'users')

urlpatterns = [
    url(r'^', include(router.urls))
]