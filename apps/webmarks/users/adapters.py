# -*- coding: utf-8 -*-
from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from rest_framework.response import Response
from allauth.account.utils import user_email
from allauth.account.utils import user_field
from allauth.account.utils import user_username
from allauth.utils import valid_email_or_none


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

    def populate_user(self,
                      request,
                      sociallogin,
                      data):
        """
        Hook that can be used to further populate the user instance.

        For convenience, we populate several common fields.

        Note that the user instance being populated represents a
        suggested User instance that represents the social user that is
        in the process of being logged in.

        The User instance need not be completely valid and conflict
        free. For example, verifying whether or not the username
        already exists, is not a responsibility.
        """
        # username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        name = data.get('name')
        user = sociallogin.user
        uid = sociallogin.account.uid
        user_username(user, uid or '')
        user_email(user, valid_email_or_none(email) or '')
        name_parts = (name or '').partition(' ')
        user_field(user, 'first_name', first_name or name_parts[0])
        user_field(user, 'last_name', last_name or name_parts[2])
        return user
