from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save
from django.conf import settings
from django.core.cache import cache

from .signals import update_cache

import os, uuid
from decimal import Decimal


class BaseManager(models.Manager):
    def get_queryset(self):
        if not cache.get(self.model._meta.db_table):
            cache.set(self.model._meta.db_table, super(BaseManager, self).get_queryset().filter(delete_flag=False),
                      settings.CACHE_TIMEOUT)
        return cache.get(self.model._meta.db_table)


class Base(models.Model):
    class Meta:
        ordering = ["-pk"]
        verbose_name_plural = "Basics"

    created_time = models.DateTimeField(db_index=True, default=now, editable=False, blank=True)
    updated_time = models.DateTimeField(db_index=True, default=now, blank=True)
    active_flag = models.BooleanField(db_index=True, default=False, help_text="Boolean")
    delete_flag = models.BooleanField(db_index=True, default=False, help_text="Boolean")
    visibility_flag = models.BooleanField(db_index=True, default=True, help_text="Boolean")
    related_parent = models.ForeignKey('self', db_index=True, related_name='related_parent_name', on_delete=models.CASCADE, blank=True, null=True)
    rate_average = models.DecimalField(db_index=True, max_digits=5, decimal_places=2, default=Decimal('0.00'))
    is_new = models.BooleanField(db_index=True, default=False, help_text='Boolean')

    objects = BaseManager()

post_save.connect(update_cache, sender=Base)


class Sms(Base):
    phone_number = models.CharField(db_index=True, max_length=11)
    code = models.CharField(db_index=True, max_length=5)

post_save.connect(update_cache, sender=Sms)


class Comment(Base):
    comment_related_parent = models.ForeignKey(Base, db_index=True, on_delete=models.CASCADE, related_name="comment_related_parent_name", blank=True, null=True)
    comment_related_user = models.ForeignKey('users.User', db_index=True, on_delete=models.CASCADE, related_name='comment_related_user_name')
    text = models.TextField()

post_save.connect(update_cache, sender=Comment)


class Rate(Base):
    rate_related_parent = models.ForeignKey(Base, db_index=True, on_delete=models.CASCADE, related_name='rate_related_parent_name')
    rate_related_user = models.ForeignKey('users.User', db_index=True, on_delete=models.CASCADE, related_name='rate_related_user_name')
    title = models.CharField(db_index=True, max_length=50, blank=True, null=True)
    value = models.DecimalField(db_index=True, max_digits=6, decimal_places=2)

post_save.connect(update_cache, sender=Rate)


class Favorite(Base):
    favorite_related_parent = models.ForeignKey(Base, db_index=True, on_delete=models.CASCADE, related_name='favorite_related_parent_name')
    favorite_related_user = models.ForeignKey('users.User', db_index=True, on_delete=models.CASCADE, related_name='favorite_related_user_name')

post_save.connect(update_cache, sender=Favorite)


class Discount(Base):
    discount_related_parent = models.ForeignKey(Base, db_index=True, on_delete=models.CASCADE, related_name='discount_related_parent_name')
    discount_related_user = models.ForeignKey('users.User', db_index=True, on_delete=models.CASCADE, related_name='discount_related_user_name')
    discount_value = models.IntegerField(db_index=True)

post_save.connect(update_cache, sender=Discount)


class ViewModel(Base):
    view_related_parent = models.ForeignKey(Base, db_index=True, on_delete=models.CASCADE, related_name='view_related_parent_name')
    view_related_user = models.ForeignKey('users.User', db_index=True, on_delete=models.CASCADE, related_name='view_related_user_name')


class Report(Base):
    report_related_parent = models.ForeignKey(Base, db_index=True, on_delete=models.CASCADE, related_name='report_related_parent_name')
    report_related_user = models.ForeignKey('users.User', db_index=True, on_delete=models.CASCADE, related_name='report_related_user_name')
    report_text = models.TextField(blank=True, null=True)

post_save.connect(update_cache, sender=Report)


def get_upload_path(media, filename):
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    return os.path.join(settings.MEDIA_ROOT, uuid.uuid4().hex + ext)


class File(Base):
    file_related_parent = models.ForeignKey(Base, db_index=True, on_delete=models.CASCADE, related_name='file_related_parent_name', blank=True, null=True)
    file_related_user = models.ForeignKey('users.User', db_index=True, on_delete=models.CASCADE, related_name='file_related_user_name')
    file_path = models.FileField(upload_to=get_upload_path)

    @property
    def file_link(self):
        return settings.MEDIA_URL + os.path.basename(self.file_path.name)

post_save.connect(update_cache, sender=File)


class Slider(Base):
    title = models.CharField(db_index=True, max_length=50, blank=True, null=True)
    link = models.CharField(db_index=True, max_length=200, blank=True, null=True)

    @property
    def image(self):
        file_instance = File.objects.filter(file_related_parent=self)
        if file_instance.count() > 0:
            return file_instance[file_instance.count() - 1].file_link
        else:
            return None

post_save.connect(update_cache, sender=Slider)


class TopFilter(Base):
    title = models.CharField(db_index=True, max_length=50, blank=True, null=True)
    link = models.CharField(db_index=True, max_length=200)
    order = models.IntegerField(db_index=True)

post_save.connect(update_cache, sender=TopFilter)
