from django.db import models
from base.models import Base, File


class Post(Base):
    post_related_user = models.ForeignKey('users.User', db_index=True, on_delete=models.CASCADE, related_name='post_related_user_name')
    title = models.CharField(db_index=True, max_length=50)
    text = models.TextField()

    @property
    def image(self):
        count = File.objects.filter(file_related_parent=self).count()
        if count > 0:
            instance = File.objects.filter(file_related_parent=self)[count - 1]
            return instance.file_link
        return None
