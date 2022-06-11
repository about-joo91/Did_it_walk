from django.urls import path
from . import views
urlpatterns = [
    path('<int:pk>',views.detail_page, name='detail_page' )
]
