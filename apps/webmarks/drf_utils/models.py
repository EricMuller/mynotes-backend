
from webmarks.users.models import User
from django.db import models


class AuditableModelMixin(models.Model):
    updated_dt = models.DateTimeField(auto_now=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    user_cre = models.ForeignKey(
        User, related_name='%(class)s_user_cre', default=None)
    user_upd = models.ForeignKey(
        User, related_name='%(class)s_user_upd', default=None, blank=True)

    class Meta:
        abstract = True
