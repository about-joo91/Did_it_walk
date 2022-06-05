from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Post(models.Model):

    class Meta:
        db_table = 'post'

    post_img_url = models.ImageField(upload_to='media/')