from django.urls import path

from posts.views import post_detail
from posts.views import PostList, PostCreate

urlpatterns = [
    path('', PostList.as_view(), name='home'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<slug:slug>/', post_detail, name='post_detail'),
]