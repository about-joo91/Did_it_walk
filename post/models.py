from distutils.command.upload import upload
from pyexpat import model
from django.db import models
from user.models import UserModel

# Create your models here.
class Posts(models.Model):
    class Meta:
        db_table = "Posts"
    contents = models.TextField()
    users = models.ForeignKey(UserModel, on_delete=models.CASCADE)

class Post_Img(models.Model):
    class Meta:
        db_table = "Post_Img"
    posts = models.ForeignKey('Posts', on_delete=models.CASCADE)
    post_img_url = models.ImageField(upload_to="media/")