from django.db import models
from django.db.models.signals import post_save
from base.models import Base, File, Discount
from base.signals import update_cache
from base.serializers import (
  FileSerializer,
  DiscountSerializer
)
from users.models import User
from stores.models import Store


class ProductCategory(Base):
    title = models.CharField(db_index=True, max_length=100)
    product_category_related_parent = models.ForeignKey('self', db_index=True, on_delete=models.CASCADE, related_name='product_category_related_parent_name', blank=True, null=True)
    product_category_related_user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE, related_name='product_category_related_user_name')
    product_category_related_store = models.ForeignKey(Store, db_index=True, on_delete=models.CASCADE, related_name='product_category_related_store_name')

    def __str__(self):
        return self.title + " - " + self.product_category_related_store.title

post_save.connect(update_cache, sender=ProductCategory)


class ProductBrand(Base):
    title = models.CharField(db_index=True, max_length=100)
    description = models.TextField(blank=True, null=True)
    product_brand_related_store = models.ForeignKey(Store, db_index=True, on_delete=models.CASCADE, related_name='product_brand_related_store_name')
    product_brand_related_user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE, related_name='product_brand_related_user_name')

    def __str__(self):
        return self.title + " - " + self.product_brand_related_store.title

post_save.connect(update_cache, sender=ProductBrand)


class Product(Base):
    title = models.CharField(db_index=True, max_length=100)
    description = models.TextField()
    product_related_store = models.ForeignKey(Store, db_index=True, on_delete=models.CASCADE, related_name='product_related_store_name')
    brand = models.CharField(max_length=50)
    product_related_category = models.ForeignKey(ProductCategory, db_index=True, on_delete=models.CASCADE, related_name='product_related_category_name')
    product_related_user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE, related_name='product_related_user_name')
    made_in_iran = models.BooleanField(db_index=True)

    def __str__(self):
        return self.title + " - " + self.product_related_store.title

    @property
    def images(self):
        file_instances = File.objects.filter(file_related_parent=self)
        serializer = FileSerializer(file_instances, many=True)
        return serializer.data

    @property
    def discount(self):
        discount_instance = Discount.objects.filter(discount_related_parent=self).order_by('-pk')
        if discount_instance.count() > 0:
            serializer = DiscountSerializer(discount_instance[0])
            return serializer.data
        return None

    @property
    def price(self):
        price_instance = ProductPrice.objects.filter(product_price_related_product=self, delete_flag=False).order_by('-pk')
        if price_instance.count() > 0:
            return price_instance[0].value
        return None

post_save.connect(update_cache, sender=Product)


class ProductPrice(Base):
    product_price_related_product = models.ForeignKey(Product, db_index=True, on_delete=models.CASCADE, related_name='product_price_related_product_name')
    amount = models.IntegerField(db_index=True)
    product_price_related_user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE, related_name='product_price_related_user')

post_save.connect(update_cache, sender=ProductPrice)
