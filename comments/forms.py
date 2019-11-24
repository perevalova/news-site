from django import forms

from comments.models import Comment


class CommentForm(forms.ModelForm):
    """
    A form for comment
    """
    class Meta:
        model = Comment
        fields = ('body',)
