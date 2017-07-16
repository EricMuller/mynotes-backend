from allauth.account.views import confirm_email as allauthemailconfirmation

from . import apiviews
from django.conf.urls import include
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # dont remove
    # otherwise -->Reverse for 'account_email_verification_sent' not found.
    # 'account_email_verification_sent' is not a valid view function or ...
    url(r'rest_auth/login/$', apiviews.login_view),
    url(r'rest_auth/login/google/$',
        csrf_exempt(apiviews.login_google_view), name='google_login'),
    url(r'rest_auth/login/linkedIn/$',
        csrf_exempt(apiviews.login_linkedin_view), name='linkedin_login'),

    url(r'rest_auth/accounts/', include('allauth.urls')),
    url(r'rest_auth/', include('rest_auth.urls')),
    url(r'rest_auth/registration/account-confirm-email/(?P<key>[\s\d\w().+-_,:&]+)/',
        allauthemailconfirmation, name="account_confirm_email"),
    url(r'rest_auth/registration/', include('rest_auth.registration.urls')),

]
