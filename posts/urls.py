from django.contrib.auth.decorators import login_required
from django.urls import path

from posts.views import PostList, PostCreate, PostDetail, BlogView, UserList, \
    UserDetail

urlpatterns = [
    path('', login_required(PostList.as_view()), name='feed'),
    path('blog/', login_required(BlogView.as_view()), name='blog'),
    path('users/', UserList.as_view(), name='users'),
    path('user/<int:pk>/', UserDetail.as_view(), name='user'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
]