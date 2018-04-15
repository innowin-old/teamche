from django.db import models
from django.utils.timezone import now

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
