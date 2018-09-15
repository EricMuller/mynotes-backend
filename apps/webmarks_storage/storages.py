import codecs
import errno
import tempfile
import os
import json
# from datetime import datetime
# from random import randint
from django.conf import settings
import os

STORE_ROOT = getattr(
    settings,
    'FILE_STORE_ROOT',
    tempfile.gettempdir() + '/store/',
)


class PathIdResolver():

    def resolvePath(self, uiid, user_name):
        index = 0
        dir_file_name = 'datas' + '/'
        # import ipdb; ipdb.set_trace()
        for character in uiid:
            if index == 4:
                dir_file_name += '/'
                index = 0
            dir_file_name += character
            index = index + 1

        return STORE_ROOT + dir_file_name + uiid


class FileStore():
    _pathIdResolver = PathIdResolver()

    def get_file_path(self, uiid, user_name):
        return self._pathIdResolver.resolvePath(uiid, user_name)

    def store(self, uiid, user_name, str_bytes, indexs):
        store_file_name = self.get_file_path(uiid, user_name)
        if not os.path.exists(os.path.dirname(store_file_name)):
            try:
                os.makedirs(os.path.dirname(store_file_name))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(store_file_name, 'wb+') as store_file:
            store_file.write(str_bytes)

        with open(store_file_name + '.idx', 'wb+') as index_file:
            json.dump(indexs, codecs.getwriter('utf-8')
                      (index_file), ensure_ascii=False)

        return store_file_name
