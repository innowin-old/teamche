from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser

from base.signals import update_cache

class User(AbstractUser):
    GENDER_CHOICES = (
      ('Female', 'female'),
      ('Male', 'male')
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')

post_save.connect(update_cache, sender=User)
