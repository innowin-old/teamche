from django.shortcuts import render
from django.db.models import Q

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.decorators import detail_route

from base.views import BaseViewSet

from .models import (
  ProductCategory,
  ProductBrand,
  Product,
  ProductPrice,
  ProductOffer
)

from .serializers import (
  ProductCategorySerializer,
  ProductCategoryAdminSerializer,
  ProductBrandSerializer,
  ProductBrandAdminSerializer,
  ProductSerializer,
  ProductListSerializer,
  ProductAdminSerializer,
  ProductAdminListSerializer,
  ProductPriceSerializer,
  ProductPriceAdminSerializer,
  ProductOfferSerializer,
  ProductOfferListSerializer
)


class ProductCategoryViewSet(BaseViewSet):
    filter_fields = ['title', 'product_category_related_parent', 'product_category_related_user', 'product_category_related_store']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = ProductCategory.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return ProductCategoryAdminSerializer
        return ProductCategorySerializer

    def perform_create(self, serializer):
        serializer.save(product_category_related_user=self.request.user)


class ProductBrandViewSet(BaseViewSet):
    filter_fields = ['title', 'product_brand_related_store', 'product_brand_related_user']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = ProductBrand.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return ProductBrandAdminSerializer
        return ProductBrandSerializer

    def perform_create(self, serializer):
        serializer.save(product_brand_related_user=self.request.user)


class ProductViewSet(BaseViewSet):
    filter_fields = ['id', 'title', 'description', 'product_related_store', 'brand', 'product_related_category', 'product_related_user', 'made_in_iran', 'rate_average', 'active_flag', 'visibility_flag']
    ordering_fields = '__all__'
    search_fields = ['title', 'description']

    def get_queryset(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            queryset = Product.objects.filter(delete_flag=False)
            #queryset = queryset.filter(Q(product_related_store__delete_flag=False, product_related_store__active_flag=True, product_related_store__visibility_flag=True) | Q(product_related_store__visibility_flag=False, product_related_user=self.request.user))
            queryset = queryset.filter(product_related_store__delete_flag=False, product_related_store__active_flag=True)
        else:
            queryset = Product.objects.filter(Q(delete_flag=False, active_flag=True) | Q(active_flag=False, product_related_user=self.request.user))
            queryset = queryset.filter(Q(product_related_store__delete_flag=False, product_related_store__active_flag=True, product_related_store__visibility_flag=True) | Q(product_related_store__visibility_flag=False, product_related_store__store_related_user=self.request.user))
            queryset = queryset.filter(Q(visibility_flag=True) | Q(visibility_flag=False, product_related_user=self.request.user))

        related_parent = self.request.query_params.get('related_parent', None)
        if related_parent is not None:
            if related_parent == 'null':
                queryset = queryset.filter(related_parent=None)
            else:
                queryset = queryset.filter(related_parent_id=related_parent)

        title__contains = self.request.query_params.get('title__contains', None)
        if title__contains is not None:
            queryset = queryset.filter(title__icontains=title__contains)

        description__contains = self.request.query_params.get('description__contains', None)
        if description__contains is not None:
            queryset = queryset.filter(description__icontains=description__contains)

        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            if self.action == 'list' or self.action == 'retrieve':
                return ProductAdminListSerializer
            return ProductAdminSerializer
        if self.action == 'list' or self.action == 'retrieve':
            return ProductListSerializer
        return ProductSerializer

    def perform_create(self, serializer):
        data = self.request.data

        if self.request and self.request.user and self.request.user.is_superuser:
            serializer.save(product_related_user=self.request.user, visibility_flag=True)
        else:
            serializer.save(product_related_user=self.request.user, is_new=True, visibility_flag=True)
        if ProductBrand.objects.filter(title=data.get('brand', ''), product_brand_related_store_id=data.get('product_related_store', ''), product_brand_related_user=self.request.user).count() == 0:
            instance = ProductBrand.objects.create(title=data.get('brand', ''), product_brand_related_store_id=data.get('product_related_store', ''), product_brand_related_user=self.request.user)

    @list_route(methods=['get'])
    def create_confirmation(self, request):
        instances = Product.objects.filter(related_parent=None, active_flag=False, delete_flag=False, is_new=True)
        instances = instances.filter(product_related_store__active_flag=True, product_related_store__delete_flag=False)
        serializer = ProductListSerializer(instances, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def update_confirmation(self, request):
        instances = Product.objects.exclude(related_parent=None).filter(active_flag=False, delete_flag=False)
        instances = instances.filter(product_related_store__active_flag=True, product_related_store__delete_flag=False)
        instances = instances.filter(related_parent__delete_flag=False)
        serializer = ProductListSerializer(instances, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def accept(self, request, pk=None):
        update_instance = self.get_object()
        if update_instance.related_parent != None and update_instance.delete_flag == False:
            instance = Product.objects.filter(id=update_instance.related_parent_id)[0]
            instance.title = update_instance.title
            instance.description = update_instance.description
            instance.product_related_store = update_instance.product_related_store
            instance.brand = update_instance.brand
            instance.product_related_category = update_instance.product_related_category
            instance.related_parent = None
            instance.active_flag = True
            instance.save()
            update_instance.delete_flag = True
            update_instance.save()
        else:
            update_instance.active_flag = True
            update_instance.save()
            instance = update_instance
        # Save price
        price_instance = ProductPrice.objects.filter(product_price_related_product=instance)
        price_instance = price_instance[price_instance.count() - 1]
        price_instance.active_flag = True
        price_instance.is_new = False
        price_instance.save()
        # Save discount
        discount_instance = Discount.objects.filter(discount_related_parent=instance)
        discount_instance = discount_instance[discount_instance.count() - 1]
        discount_instance.active_flag = True
        discount_instance.is_new = False
        discount_instance.save()
        # Return serializer data
        serializer = ProductSerializer(instance)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def deny(self, request, pk=None):
        instance = self.get_object()
        instance.delete_flag = True
        instance.save()
        return Response({'status': 'Store Denied.'})


class ProductPriceViewSet(BaseViewSet):
    filter_fields = ['product_price_related_product', 'amount', 'product_price_related_user']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = ProductPrice.objects.filter(delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.request and self.request.user and self.request.user.is_superuser:
            return ProductPriceAdminSerializer
        return ProductPriceSerializer

    def perform_create(self, serializer):
        if self.request and self.request.user and self.request.user.is_superuser:
            serializer.save(product_price_related_user=self.request.user, active_flag=True)
        else:
            serializer.save(product_price_related_user=self.request.user, active_flag=False, is_new=True)


class ProductOfferViewSet(BaseViewSet):
    filter_fields = ['start_date', 'end_date', 'active_flag', 'visibility_flag']
    ordering_fields = '__all__'

    def get_queryset(self):
        queryset = ProductOffer.objects.filter(delete_flag=False)
        queryset = queryset.filter(product_offer_related_product__active_flag=True, product_offer_related_product__delete_flag=False)
        queryset = queryset.filter(product_offer_related_product__product_related_store__active_flag=True)
        queryset = queryset.filter(product_offer_related_product__product_related_store__delete_flag=False)
        return queryset

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductOfferListSerializer
        return ProductOfferSerializer

    def perform_create(self, serializer):
        serializer.save(is_new=True, visibility_flag=True)

    @list_route(methods=['get'])
    def create_confirmation(self, request):
        instances = ProductOffer.objects.filter(related_parent=None, active_flag=False, delete_flag=False, is_new=True)
        instances = instances.filter(product_offer_related_product__delete_flag=False, product_offer_related_product__active_flag=True)
        instances = instances.filter(product_offer_related_product__product_related_store__delete_flag=False)
        instances = instances.filter(product_offer_related_product__product_related_store__active_flag=True)
        serializer = ProductOfferSerializer(instances, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def update_confirmation(self, request):
        instances = ProductOffer.objects.exclude(related_parent=None).filter(active_flag=False, delete_flag=False)
        instances = instances.filter(product_offer_related_product__delete_flag=False, product_offer_related_product__active_flag=True)
        instances = instances.filter(product_offer_related_product__product_related_store__active_flag=True)
        instances = instances.filter(product_offer_related_product__product_related_store__delete_flag=False)
        serializer = ProductOfferSerializer(instances, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def accept(self, request, pk=None):
        instance = self.get_object()
        if instance.related_parent != None:
            instance.delete_flag = True
            instance.is_new = False
            instance.save()
            update_instance = instance.related_parent
            update_instance.reason = instance.reason
            update_instance.start_date = instance.start_date
            update_instance.end_date = instance.end_date
            update_instance.active_flag = True
            update_instance.is_new = False
            update_instance.save()
            serializer = ProductOfferSerializer(update_instance)
            return Response(serializer.data)
        instance.active_flag = True
        instance.is_new = False
        instance.save()
        serializer = ProductOfferSerializer(instance)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def deny(self, request, pk=None):
        instance = self.get_object()
        instance.delete_flag = True
        instance.is_new = False
        instance.save()
        serializer = ProductOfferSerializer(instance)
        return Response(serializer.data)
