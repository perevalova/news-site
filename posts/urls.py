from django.contrib.auth.decorators import login_required
from django.urls import path

from posts.views import PostList, PostCreate, PostDetail, BlogView

urlpatterns = [
    path('', login_required(PostList.as_view()), name='feed'),
    path('blog/', login_required(BlogView.as_view()), name='blog'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<slug:slug>/', PostDetail.as_view(), name='post_detail'),
]