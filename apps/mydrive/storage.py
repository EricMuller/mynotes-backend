

import errno
import tempfile
import os

# from datetime import datetime
# from random import randint
from django.conf import settings

STORE_ROOT = getattr(
    settings,
    'STORE_ROOT',
    tempfile.gettempdir() + '/store/',
)


class PathResolver():

    def resolvePath(self, id, filename):
        file_name, file_extension = os.path.splitext(filename)
        new_full_name = file_name
        return os.path.join(STORE_ROOT, str(id), new_full_name)


class FileStore():

    _pathResolver = PathResolver()

    def store(self, id, file):
        store_file_name = self._pathResolver.resolvePath(id, file.name)
        if not os.path.exists(os.path.dirname(store_file_name)):
            try:
                os.makedirs(os.path.dirname(store_file_name))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        store_file = open(store_file_name, 'wb+')
        for chunk in file.chunks():
            store_file.write(chunk)
        store_file.close()
        return store_file_name
