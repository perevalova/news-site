from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import CreateView, ListView
from django.views.generic.base import View

from comments.forms import CommentForm
from posts.forms import PostCreateForm
from posts.models import Post
from posts.tasks import send_comment_email


class PostList(ListView):
    """
    Showing all posts
    """
    model = Post
    template_name = 'main.html'
    context_object_name = 'post_list'
    paginate_by = 5
    queryset = Post.approved.all()


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
            post.status = Post.APPROVE
        post.save()
        return redirect(post)


class PostDetail(View):

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'])
        comments = post.comments.all()
        form = CommentForm()
        return render(request, 'post_detail.html',
                      {'post': post, 'comments': comments, 'form': form})

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'])
        comments = post.comments.all()
        form = CommentForm(data=request.POST)
        if form.is_valid():

            # Create Comment object but don't save to database yet
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()

            # Send email
            user = post.author
            mail_subject = 'New comment'
            message = render_to_string('new_comment.html', {
                'user': user,
                'author': comment.author,
            })
            to_email = [user.email]
            send_comment_email.delay(mail_subject, message, to_email)
            return redirect('post_detail', slug=post)
        else:
            return render(request, 'post_detail.html',
                          {'post': post, 'comments': comments, 'form': form})


class BlogView(ListView):
    """
    Personal blog view
    """
    model = Post
    template_name = 'blog.html'
    paginate_by = 5
#
    def get_queryset(self):
        posts = Post.approved.filter(author=self.request.user)
        return posts
