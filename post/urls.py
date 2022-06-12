from django.urls import path
from . import views
from detail_page.urls import urlpatterns

urlpatterns = [
    path('', views.home, name='home'),
    path('post_images/<obj_id>', views.show_image, name='post_images'),
    path('home/<str:page_name>', views.main, name = 'recent2'),
    path('like/<int:post_id>', views.like, name ='like_post'),
    path('comment/<int:post_id>', views.comment, name ='comment'),
    path('comment/<int:post_id>/<int:comment_id>', views.comment, name='comment'),
    path('comment/edit/<int:comment_id>', views.comment_edit, name='comment_edit'),
]
