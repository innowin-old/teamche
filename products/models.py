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
        return str(self.id) + '. ' + self.title + " - " + self.product_category_related_store.title

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
        return str(self.id) + '. ' + self.title + " - " + self.product_related_store.title

    @property
    def images(self):
        file_instances = File.objects.filter(file_related_parent=self)
        serializer = FileSerializer(file_instances, many=True)
        return serializer.data

    @property
    def discount(self):
        if self.related_parent == None:
            discount_instance = Discount.objects.filter(discount_related_parent=self, active_flag=True, delete_flag=False, is_new=False)
        else:
            discount_instance = Discount.objects.filter(discount_related_parent=self.related_parent, is_new=True)
        if discount_instance.count() > 0:
            serializer = DiscountSerializer(discount_instance[discount_instance.count() - 1])
            return serializer.data
        return 0

    @property
    def price(self):
        if self.related_parent == None:
            price_instance = ProductPrice.objects.filter(product_price_related_product=self, delete_flag=False, active_flag=True, is_new=False)
        else:
            price_instance = ProductPrice.objects.filter(product_price_related_product=self.related_parent, delete_flag=False, is_new=True)
        if price_instance.count() > 0:
            return price_instance[price_instance.count() - 1].amount
        return 0

post_save.connect(update_cache, sender=Product)


class ProductPrice(Base):
    product_price_related_product = models.ForeignKey(Product, db_index=True, on_delete=models.CASCADE, related_name='product_price_related_product_name')
    amount = models.IntegerField(db_index=True)
    product_price_related_user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE, related_name='product_price_related_user')

post_save.connect(update_cache, sender=ProductPrice)



class ProductOffer(Base):
    product_offer_related_product = models.ForeignKey(Product, db_index=True, on_delete=models.CASCADE, related_name='product_offer_related_product_name')
    reason = models.TextField()
    start_date = models.IntegerField(db_index=True)
    end_date = models.IntegerField(db_index=True)
