from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from rest_framework.routers import SimpleRouter

from .views import (
    SmsViewSet,
    CommentViewSet,
    RateViewSet,
    FavoriteViewSet,
    DiscountViewSet,
    ViewModelViewSet,
    ReportViewSet,
    FileViewSet,
    SliderViewSet,
    TopFilterViewSet
)

router = SimpleRouter()
router.register(r'comments', CommentViewSet, 'base-comments')
router.register(r'sms', SmsViewSet, 'base-sms')
router.register(r'rates', RateViewSet, 'base-rates')
router.register(r'favorites', FavoriteViewSet, 'base-favorites')
router.register(r'discounts', DiscountViewSet, 'base-discounts')
router.register(r'reports', ReportViewSet, 'base-reports')
router.register(r'files', FileViewSet, 'base-files')
router.register(r'sliders', SliderViewSet, 'base-sliders')
router.register(r'views', ViewModelViewSet, 'base-views')
router.register(r'top-filters', TopFilterViewSet, 'base=top=filters')

urlpatterns = [
    url(r'^', include(router.urls))
]
