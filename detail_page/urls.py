from django.urls import path
from . import views


urlpatterns = [
    path('<int:pk>',views.DetailView.as_view(), name='detail_page'),
    path('like/<int:post_id>', views.LikeView.as_view(), name='detail_like'),
]
