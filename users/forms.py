from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import FormActions

from .models import CustomUser


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class UserSignupForm(UserCreationForm):
    """
    Form for Custom User authentication
    """
    class Meta:
        model = CustomUser
        fields = ['email', 'password1', 'password2', 'first_name', 'last_name', 'birthday']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # form tag attributes
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'POST'
        self.helper.form_action = 'signup'

        # twitter bootstrap styles
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-6'

        self.helper.layout = Layout(
            'email', 'password1', 'password2', 'first_name', 'last_name', 'birthday',
            FormActions(
                Submit('save_button', 'Sign Up', css_class="btn btn-primary"),
            )
        )
