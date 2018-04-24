from django.conf.urls import url, include
from rest_framework.routers import SimpleRouter

from .views import (
  ProductCategoryViewSet,
  ProductBrandViewSet,
  ProductViewSet,
  ProductPriceViewSet
)


router = SimpleRouter()
router.register(r'categories', ProductCategoryViewSet, 'product-categories')
router.register(r'brands', ProductBrandViewSet, 'product-brands')
router.register(r'prices', ProductPriceViewSet, 'product-prices')
router.register(r'', ProductViewSet, 'products')

urlpatterns = [
  url(r'^', include(router.urls))
]
