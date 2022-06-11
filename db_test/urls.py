from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommend_shoes, name='recommend_shoes'),
    path('specific/', views.get_specific_shoes, name='get_specific')
]
