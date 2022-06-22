from django.urls import path
from . import views
from detail_page.urls import urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('home/<str:page_name>', views.main, name = 'recent2'),
    path('like/<int:post_id>', views.LikeView.as_view(), name ='like_post'),
    path('comment/<int:pk>', views.ComentView.as_view(), name ='comment'),
    path('home/recent/edit_content/<int:post_id>', views.edit_content, name="edit_content"),
    path('delete/<int:post_id>', views.delete_content, name="delete_content"),
]
