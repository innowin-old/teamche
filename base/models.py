from django.db import models
from django.utils.timezone import now
from users.models import User

class Base(models.Model):
    class Meta:
        ordering = ["-pk"]
        verbose_name_plural = "Basics"

    created_time = models.DateTimeField(db_index=True, default=now, editable=False, blank=True)
    updated_time = models.DateTimeField(db_index=True, default=now, blank=True)
    delete_flag = models.BooleanField(db_index=True, default=False, help_text="Boolean")


class Sms(Base):
    phone_number = models.CharField(max_length=11)
    code = models.CharField(max_length=5)


class Comment(Base):
    related_parent = models.ForeignKey(Base, on_delete=models.CASCADE, related_name="comment_related_base")
    text = models.TextField()


class Rate(Base):
    rate_related_parent = models.ForeignKey(Base, on_delete=models.CASCADE, related_name='rate_related_parent_name')
    rate_related_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rate_related_user_name')
    title = models.CharField(max_length=50, blank=True, null=True)
    value = models.DecimalField(max_digits=6, decimal_places=2)
