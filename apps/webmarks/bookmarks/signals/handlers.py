
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from webmarks.bookmarks.models import Bookmark
from webmarks.drf_utils.cache import cache_updated_api_at
from webmarks.bookmarks.channels.publishers import ws_model_saved_at
from webmarks.bookmarks.channels.publishers import ws_model_deleted_at


for model in [Bookmark]:
    post_save.connect(receiver=cache_updated_api_at, sender=model)
    post_delete.connect(receiver=cache_updated_api_at, sender=model)

for model in [Bookmark]:
    post_save.connect(receiver=ws_model_saved_at, sender=model)
    post_delete.connect(receiver=ws_model_deleted_at, sender=model)
