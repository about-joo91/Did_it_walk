from django.urls import path
from . import views
urlpatterns = [
    path('', views.likes_test, name ='likes_test'),
    path('<int:post_id>/', views.like_post, name ='like_post'),
]
