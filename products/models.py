from django.db import models
from django.db.models.signals import post_save
from base.models import Base
from base.signals import update_cache
from users.models import User
from stores.models import Store


class ProductCategory(Base):
    title = models.CharField(max_length=100)
    product_category_related_parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='product_category_related_parent_name', blank=True, null=True)
    product_category_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_category_related_user_name')
    product_category_related_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_category_related_store_name')

    def __str__(self):
        return self.title + " - " + self.product_category_related_store.title

post_save.connect(update_cache, sender=ProductCategory)


class ProductBrand(Base):
    title = models.CharField(max_length=100)
    product_brand_related_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_brand_related_store_name')
    product_brand_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_brand_related_user_name')

    def __str__(self):
        return self.title + " - " + self.product_brand_related_store.title

post_save.connect(update_cache, sender=ProductBrand)


class Product(Base):
    title = models.CharField(max_length=100)
    product_related_store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='product_related_store_name')
    brand = models.CharField(max_length=50)
    product_related_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='product_related_category_name')
    product_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_related_user_name')
    made_in_iran = models.BooleanField()

    def __str__(self):
        return self.title + " - " + self.product_related_store.title

post_save.connect(update_cache, sender=Product)


class ProductPrice(Base):
    product_price_related_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_price_related_product_name')
    amount = models.IntegerField()
    product_price_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product_price_related_user')

post_save.connect(update_cache, sender=ProductPrice)
