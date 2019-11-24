from django.urls import path, include

from users.views import UserSignup, Activate

urlpatterns = [
    path('accounts/signup/', UserSignup.as_view(), name='signup'),
    path('activate/<str:uidb64>/<str:token>', Activate.as_view(), name='activate'),
    path('accounts/', include('django.contrib.auth.urls')),
]
