from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    GENDER_CHOICES = (
      ('Female', 'female'),
      ('Male', 'male')
    )
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
