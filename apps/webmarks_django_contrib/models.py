
from django.db import models
from django.conf import settings


class AuditableModelMixin(models.Model):
    updated_dt = models.DateTimeField(auto_now=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    user_cre = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_user_cre', default=None)
    user_upd = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='%(class)s_user_upd', default=None, blank=True)

    class Meta:
        abstract = True
