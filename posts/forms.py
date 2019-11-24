from ckeditor.widgets import CKEditorWidget
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from django import forms
from django.urls import reverse

from posts.models import Post


class PostCreateForm(forms.ModelForm):
    """
    Form for creation a post
    """
    class Meta:
        model = Post
        fields = ('title', 'content', 'attachment')
        attachment = forms.CharField(widget=CKEditorWidget())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # this helper object allows us to customize a form
        self.helper = FormHelper(self)

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = reverse('post_create')

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper.layout = Layout(
             'title', 'content', 'attachment',
            FormActions(
                Submit('save_button', 'Save', css_class="btn btn-primary"),
            )
        )
