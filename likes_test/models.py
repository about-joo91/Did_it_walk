from django.db import models
from user.models import UserModel
from post.models import Post
# Create your models here.

class Likes(models.Model):
    class Meta:
        db_table = 'likes'
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
