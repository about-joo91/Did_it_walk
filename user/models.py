from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.

class UserModel(AbstractUser):
    class Meta:
        db_table = 'my_user'
    nickname = models.CharField(max_length=128,unique=True, null=True)
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')
    profile_url = models.URLField(default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973461_960_720.png')