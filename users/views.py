from users.forms import UserSignupForm
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.views import View
from django.shortcuts import render

from users.models import CustomUser
from users.token_generator import account_activation_token
from users.tasks import send_confirm_email


class UserLogin(LoginView):
    """
    A view for Custom User authentication
    """
    model = CustomUser
    template_name = 'registration/login.html'


class UserSignup(View):
    """
    A view for Custom User registration
    """
    def get(self, request):
        form = UserSignupForm()
        return render(request, 'registration/signup.html', {'form': form})

    def post(self, request):
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Send an email to the user with the token:
            mail_subject = 'Activate your account.'
            current_site = get_current_site(request)
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            # send_mail(mail_subject, message, 'test@newssite.com', [to_email])

            send_confirm_email.delay(mail_subject, message, to_email)
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            form = UserSignupForm()


class Activate(View):
    """
    User activation by confirmation link
    """
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return HttpResponse('Your account has been activate successfully')
        else:
            return HttpResponse('Activation link is invalid!')
