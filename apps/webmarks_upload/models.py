from webmarks_social.models import User
from django.db import models


class Upload(models.Model):
    TYPES = (
        ('FAVORITE', 'Favorite'),
    )
    file = models.FileField()
    type = models.CharField(max_length=10, choices=TYPES)
    # name is filename without extension
    name = models.CharField(max_length=100)
    version = models.IntegerField(default=0)
    upload_date = models.DateTimeField(auto_now=True, db_index=True)
    owner = models.ForeignKey(User, related_name='uploaded_files')
    size = models.IntegerField(default=0)
