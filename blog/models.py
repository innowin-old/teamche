from django.db import models
from base.models import Base


class Post(Base):
    post_related_user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='post_related_user_name')
    title = models.CharField(max_length=50)
    text = models.TextField()
