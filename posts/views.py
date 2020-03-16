from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.generic import CreateView, ListView, DetailView
from django.views.generic.base import View

from comments.forms import CommentForm
from posts.forms import PostCreateForm
from posts.models import Post, PersonalBlog
from posts.tasks import send_comment_email


class PostList(ListView):
    """
    Showing posts of subscriptions
    """
    model = Post
    template_name = 'feed.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        blog = PersonalBlog.objects.get(author_id=self.request.user.id)
        posts = Post.approved.filter(
            author__in=blog.subscriptions.all()).select_related('author')
        return posts

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blog'] = PersonalBlog.objects.prefetch_related(
            'read_posts').get(author_id=self.request.user.id)
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
            post.status = Post.APPROVE
        post.save()
        return redirect(post)


class PostDetail(View):

    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'])
        comments = post.comments.all()
        form = CommentForm()
        blog = PersonalBlog.objects.get(author_id=self.request.user.id)
        return render(request, 'post_detail.html',
                      {'post': post, 'comments': comments, 'form': form, 'blog': blog})

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, slug=kwargs['slug'])
        comments = post.comments.all()
        form = CommentForm(data=request.POST)

        # mark post as read
        action = request.POST.get('action')
        if action:
            current_blog = PersonalBlog.objects.get(
                author_id=self.request.user.id)
            current_blog.read_posts.add(post)
            return JsonResponse({'status': 'ok'})
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

    def get_queryset(self):
        posts = Post.approved.filter(author=self.request.user)
        return posts


class UserList(ListView):
    model = PersonalBlog
    template_name = 'user_list.html'
    queryset = PersonalBlog.objects.all().select_related('author')


class UserDetail(DetailView):
    model = PersonalBlog
    template_name = 'user_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post_list'] = Post.approved.filter(author_id=self.object.id).select_related('author')
        # check if current user follow selected user blog
        subscriptions = PersonalBlog.objects.get(author_id=self.request.user.id).subscriptions.all()
        context['following'] = True if self.object.author in subscriptions else False

        return context

    def post(self, request, *args, **kwargs):
        """
        Add or remove subscription
        """
        action = request.POST.get('action')
        user_pk = request.POST.get('pk')
        if action and user_pk:
            current_blog = PersonalBlog.objects.get(
                author_id=self.request.user.id)
            User = get_user_model()
            user_blog = User.objects.get(id=user_pk)
            if action == 'follow':
                current_blog.subscriptions.add(user_blog)
            else:
                current_blog.subscriptions.remove(user_blog)
            return JsonResponse({'status': 'ok'})