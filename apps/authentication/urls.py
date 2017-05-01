# from allauth.socialaccount.providers.facebook.views import login_by_token
from allauth.account.views import confirm_email as allauthemailconfirmation

from apps.authentication import apiviews
from django.conf.urls import include
from django.conf.urls import url
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # url(r'^api/v1/signup/facebook$',
    #     csrf_exempt(apiviews.FacebookLoginOrSignup.as_view()),
    #     name='facebook-login-signup'),
    # url(r'^api/authenticate', obtain_auth_token),
    # url(r'^api-token-auth/', apiviews.obtain_auth_token),
    # url(r'^auth/', include('rest_framework_social_oauth2.urls')),

    # dont remove
    # otherwise -->Reverse for 'account_email_verification_sent' not found.
    # 'account_email_verification_sent' is not a valid view function or ...
    url(r'^accounts/', include('allauth.urls')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/account-confirm-email/(?P<key>[\s\d\w().+-_,:&]+)/$',
        allauthemailconfirmation, name="account_confirm_email"),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^rest-auth/token/', apiviews.obtain_auth_token),
]
