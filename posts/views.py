from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import CreateView, TemplateView

from comments.forms import CommentForm
from posts.forms import PostCreateForm
from posts.models import Post
from posts.tasks import send_comment_email


class PostList(TemplateView):
    """
    Showing all posts
    """
    # queryset = Post.objects.filter(status='APPROVE').order_by('-created_on')
    template_name = 'main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objects = Post.approved.order_by('-created_on')
        paginator = Paginator(objects, 5)

        # try to get page number from request
        page = self.request.GET.get('page', 1)
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            # if page is not an integer, deliver first page
            object_list = paginator.page(1)
        except EmptyPage:
            # if page is out of range (e.g. 9999),
            # deliver last page of results
            object_list = paginator.page(paginator.num_pages)

        # set variables into context
        context['post_list'] = object_list
        context['is_paginated'] = object_list.has_other_pages()
        context['page_obj'] = object_list
        context['paginator'] = paginator

        return context


class PostCreate(LoginRequiredMixin, CreateView):
    """
    Creation a post
    """
    model = Post
    template_name = 'post_create.html'
    form_class = PostCreateForm

    def form_valid(self, form):
        post = form.save(commit=False)

        # Save a post with auth user
        post.author = self.request.user

        # Save post with an 'approve' status for 'admins' and 'editors' groups
        group = self.request.user.groups.values_list('name').first()[0]
        if group == 'admins' or group == 'editors':
            post.status = 'APPROVE'
        post.save()
        return redirect(post)


def post_detail(request, slug):
    """
    Showing a detail post with comments
    """
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            comment.post = post
            # Save a post with auth user
            comment.author = request.user
            # Save the comment to the database
            comment.save()

            # Send email
            user = post.author
            mail_subject = 'New comment'
            message = f'{comment.author} left comment on your post'
            to_email = [user.email]
            send_comment_email.delay(mail_subject, message, to_email)
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'comment_form': comment_form})
