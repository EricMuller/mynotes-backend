# -*- coding: utf-8 -*-
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework.response import Response


class MailError(Exception):
    """
    The exception used for mail errors during send mail.
    """
    pass


class AccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)

    def respond_user_inactive(self, request, user):
        return Response({'message': 'respond_user_inactive'})

    def respond_email_verification_sent(self, request, user):
        return Response({'message': 'account_email_verification_sent'})

    def send_mail(self, template_prefix, email, context):
        try:
            msg = self.render_mail(template_prefix, email, context)
            msg.send()

        except:
            raise MailError('Error while sending confirmation mail')


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    def is_open_for_signup(self, request, sociallogin):
        return getattr(settings, 'ACCOUNT_ALLOW_REGISTRATION', True)
