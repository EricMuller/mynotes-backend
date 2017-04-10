import datetime
from django.core.cache import cache
from django.utils.encoding import force_text
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from apps.mynotes.models import Note

from rest_framework_extensions.key_constructor.constructors import (
    DefaultKeyConstructor
)

from rest_framework_extensions.key_constructor.bits import (
    KeyBitBase,
    ListSqlQueryKeyBit,
    PaginationKeyBit
)


class UpdatedAtKeyBit(KeyBitBase):
    def get_data(self, **kwargs):
        key = 'api_updated_at_timestamp'
        value = cache.get(key, None)
        if not value:
            value = datetime.datetime.utcnow()
            cache.set(key, value=value)
        return force_text(value)


class CustomListKeyConstructor(DefaultKeyConstructor):
    list_sql = ListSqlQueryKeyBit()
    pagination = PaginationKeyBit()
    updated_at = UpdatedAtKeyBit()


def change_api_updated_at(sender=None, instance=None, *args, **kwargs):
    cache.set('api_updated_at_timestamp', datetime.datetime.utcnow())


for model in [Note]:
    post_save.connect(receiver=change_api_updated_at, sender=model)
    post_delete.connect(receiver=change_api_updated_at, sender=model)
