
from django.db.models.signals import post_delete
from django.db.models.signals import post_save
from apps.mywebmarks.models import Media
from apps.mywebmarks.cache import cache_updated_api_at
from apps.mywebmarks.channels.publishers import ws_model_saved_at
from apps.mywebmarks.channels.publishers import ws_model_deleted_at


for model in [Media]:
    post_save.connect(receiver=cache_updated_api_at, sender=model)
    post_delete.connect(receiver=cache_updated_api_at, sender=model)

for model in [Media]:
    post_save.connect(receiver=ws_model_saved_at, sender=model)
    post_delete.connect(receiver=ws_model_deleted_at, sender=model)
