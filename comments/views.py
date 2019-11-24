from django.views.generic import CreateView

from comments.forms import CommentForm
from comments.models import Comment


class CommentCreate(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments.html'