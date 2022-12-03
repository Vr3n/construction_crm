from django.urls import path, include, re_path
from dj_rest_auth.registration.views import VerifyEmailView
from allauth.account.views import ConfirmEmailView
from .views import login, logout


urlpatterns = [
    path('accounts/', include('allauth.urls')),

    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),

    # path('', include('dj_rest_auth.urls')),
    # re_path(
    #     r'^accounts/register/account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(
    #     ),
    #     name='account_confirm_email',
    # ),
    path('accounts/register/', include('dj_rest_auth.registration.urls')),
    path('account-confirm-email/', VerifyEmailView.as_view(),
         name="account_email_verification_sent"),
]
