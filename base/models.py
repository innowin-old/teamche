from django.db import models
from django.utils.timezone import now
from django.db.models.signals import post_save

from users.models import User
from .signals import update_cache


class Base(models.Model):
    class Meta:
        ordering = ["-pk"]
        verbose_name_plural = "Basics"

    created_time = models.DateTimeField(db_index=True, default=now, editable=False, blank=True)
    updated_time = models.DateTimeField(db_index=True, default=now, blank=True)
    delete_flag = models.BooleanField(db_index=True, default=False, help_text="Boolean")

post_save.connect(update_cache, sender=Base)


class Sms(Base):
    phone_number = models.CharField(max_length=11)
    code = models.CharField(max_length=5)

post_save.connect(update_cache, sender=Sms)


class Comment(Base):
    comment_related_parent = models.ForeignKey(Base, on_delete=models.CASCADE, related_name="comment_related_parent_name")
    comment_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_related_user_name')
    text = models.TextField()

post_save.connect(update_cache, sender=Comment)


class Rate(Base):
    rate_related_parent = models.ForeignKey(Base, on_delete=models.CASCADE, related_name='rate_related_parent_name')
    rate_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rate_related_user_name')
    title = models.CharField(max_length=50, blank=True, null=True)
    value = models.DecimalField(max_digits=6, decimal_places=2)

post_save.connect(update_cache, sender=Rate)


class Favorite(Base):
    favorite_related_parent = models.ForeignKey(Base, on_delete=models.CASCADE, related_name='favorite_related_parent_name')
    favorite_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_related_user_name')

post_save.connect(update_cache, sender=Favorite)


class Discount(Base):
    discount_related_parent = models.ForeignKey(Base, on_delete=models.CASCADE, related_name='discount_related_parent_name')
    discount_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discount_related_user_name')
    discount_value = models.IntegerField()

post_save.connect(update_cache, sender=Discount)


class Report(Base):
    report_related_parent = models.ForeignKey(Base, on_delete=models.CASCADE, related_name='report_related_parent_name')
    report_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_related_user_name')
    report_text = models.TextField(blank=True, null=True)

post_save.connect(update_cache, sender=Report)
