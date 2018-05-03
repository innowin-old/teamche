from django.db import models
from django.db.models.signals import post_save

from base.models import Base, File, Favorite
from users.models import User
from base.signals import update_cache


class StoreCategory(Base):
    title = models.CharField(max_length=50)

    def image(self):
        file_instance = File.objects.filter(file_related_parent=self)
        if file_instance.count() > 0:
            return file_instance[0].file_link
        else:
            return None

post_save.connect(update_cache, sender=StoreCategory)


class Store(Base):
    title = models.CharField(max_length=100)
    description = models.TextField()
    store_related_category = models.ForeignKey(StoreCategory, related_name="store_related_category_name", on_delete=models.CASCADE)
    store_related_owner = models.ForeignKey(User, related_name="store_related_owner_name", on_delete=models.CASCADE, blank=True, null=True)
    store_related_user = models.ForeignKey(User, related_name='store_related_user_name', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, blank=True, null=True)
    latitude = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    longitude = models.DecimalField(max_digits=19, decimal_places=10, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    active_flag = models.BooleanField(default=False)
    related_logo = models.ForeignKey('base.File', on_delete=models.CASCADE, related_name="store_related_logo_name", blank=True, null=True)

    @property
    def images(self):
        images = []
        files = File.objects.filter(file_related_parent=self)
        for file in files:
            data = {'link': file.file_link}
            images.append(data)
        return images

post_save.connect(update_cache, sender=Store)


class StoreVisit(Base):
    store_visit_related_store = models.ForeignKey(Store, related_name='store_visit_related_store', on_delete=models.CASCADE)
    store_visit_related_user = models.ForeignKey(User, related_name='store_visit_related_user', on_delete=models.CASCADE)
    active_flag = models.BooleanField(default=False)

post_save.connect(update_cache, sender=StoreVisit)
