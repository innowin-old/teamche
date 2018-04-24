from django.db import models
from base.models import Base
from users.models import User
from stores.models import Store


class ProductCategory(Base):
    title = models.CharField(max_length=100)
    product_category_related_parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='product_category_related_parent_name', blank=True, null=True)
    product_category_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_category_related_user_name')


class ProductBrand(Base):
    title = models.CharField(max_length=100)
    product_brand_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_brand_related_user_name')


class Product(Base):
    title = models.CharField(max_length=100)
    product_related_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_related_store_name')
    product_related_brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, related_name='product_related_brand_name')
    product_related_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='product_related_category_name')
    product_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_related_user_name')
    made_in_iran = models.BooleanField()


class ProductPrice(Base):
    product_price_related_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_price_related_product_name')
    amount = models.IntegerField()
