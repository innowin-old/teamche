from django.db import models
from base.models import Base


class Post(Base):
    post_related_user = models.ForeignKey('users.User', db_index=True, on_delete=models.CASCADE, related_name='post_related_user_name')
    title = models.CharField(db_index=True, max_length=50)
    text = models.TextField()
