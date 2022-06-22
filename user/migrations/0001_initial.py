# Generated by Django 4.0.5 on 2022-06-22 02:52

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=20, unique=True, verbose_name='username')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=128, verbose_name='email')),
                ('fullname', models.CharField(max_length=20, verbose_name='fullname')),
                ('nickname', models.CharField(max_length=128, null=True, unique=True)),
                ('profile_url', models.URLField(default='https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973461_960_720.png')),
                ('join_date', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='updated_at')),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('follow', models.ManyToManyField(related_name='followee', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
