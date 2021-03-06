from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import SimpleRouter

from .views import (
    StoreViewSet,
    StoreCategoryViewSet,
    StoreVisitViewSet
  )

router = SimpleRouter()
router.register(r'categories', StoreCategoryViewSet, 'categories')
router.register(r'visits', StoreVisitViewSet, 'visits')
router.register(r'', StoreViewSet, 'stores')

urlpatterns = [
    url(r'^', include(router.urls))
]
