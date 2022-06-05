from distutils.command.upload import upload
from django.db import models

# Create your models here.
class Post(models.Model):

    class Meta:
        db_table = 'post'

    title = models.CharField(max_length=128)
    cover = models.ImageField(upload_to='media/')