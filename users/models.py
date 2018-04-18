from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

from base.models import Base
from base.signals import update_cache

class User(AbstractUser, Base):
    GENDER_CHOICES = (
      ('female', 'Female'),
      ('male', 'Male')
    )
    MEMBER_TYPE_CHOICES = (
      ('normal', 'Normal'),
      ('specific', 'Specific'),
      ('gold', 'Gold')
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
    type = models.CharField(max_length=8, choices=MEMBER_TYPE_CHOICES, default='normal')

post_save.connect(update_cache, sender=User)
