from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import SimpleRouter

from .views import (
  PostViewSet
)

router = SimpleRouter()
router.register(r'', PostViewSet, 'blog-posts')

urlpatterns = [
  url(r'^', include(router.urls))
]
