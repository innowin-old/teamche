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
    gender = models.CharField(db_index=True, max_length=6, choices=GENDER_CHOICES, default='male')
    type = models.CharField(db_index=True, max_length=8, choices=MEMBER_TYPE_CHOICES, default='normal')

post_save.connect(update_cache, sender=User)


class UpgradeRequest(Base):
    GENDER_CHOICES = (
      ('female', 'Female'),
      ('male', 'Male')
    )
    MEMBER_TYPE_CHOICES = (
      ('normal', 'Normal'),
      ('specific', 'Specific'),
      ('gold', 'Gold')
    )
    upgrade_request_related_user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE, related_name='upgrade_request_related_user_name')
    first_name = models.CharField(db_index=True, max_length=50)
    last_name = models.CharField(db_index=True, max_length=100)
    gender = models.CharField(db_index=True, max_length=6, choices=GENDER_CHOICES)
    type = models.CharField(db_index=True, max_length=8, choices=MEMBER_TYPE_CHOICES, default='specific')

    def member_type(self):
        return self.upgrade_request_related_user.type

post_save.connect(update_cache, sender=UpgradeRequest)



class FCMToken(Base):
    fcm_token_related_user = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE, related_name='fcm_token_related_user_name')
    token = models.CharField(max_length=256)
