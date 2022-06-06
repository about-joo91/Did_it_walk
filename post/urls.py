from re import template
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.main, name='main'),
    path('post_images/<int:obj_id>', views.show_image, name='post_images/<int:pk>'),
]
