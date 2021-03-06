from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self,username, password=None):
        if not username:
            raise ValueError('아이디가 공란이어서 곤란합니다.')
        user = self.model(
            username = username
        )
        user.set_password(password)
        user.save(using = self._db)
        return user
    def create_superuser(self, username, password=None):
        user =self.create_user(
            username= username,
            password= password
        )
        user.is_admin = True
        user.save(using= self._db)
        return user
    
# Create your models here.
class UserModel(AbstractBaseUser):
    username = models.CharField('username' , max_length=20, unique=True)
    password  = models.CharField('password', max_length=128)
    nickname = models.CharField(max_length=128,unique=True, null=True)
    follow = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followee')

    profile_url = models.URLField(default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973461_960_720.png')
    
    join_date = models.DateTimeField('created_at', auto_now_add=True)
    updated_at = models.DateField('updated_at', auto_now=True)

    is_active = models.BooleanField(default=True)

    is_admin =models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    objects = UserManager()

    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def has_perm(self,perm,obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


    