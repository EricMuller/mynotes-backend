
import logging
from channels import Channel
from channels import Group
from json import dumps
from rest_framework.authtoken.models import Token
from webmarks_bookmarks.serializers import PublishedModelSerializer

stdlogger = logging.getLogger(__name__)


class Message:
    def __init__(self, message):
        self.event = GroupPublisher.EVENTS['MESSAGE']
        self.data = message

    def as_dict(self):
        return self.__dict__


class GroupPublisher:

    EVENTS = {
        'MESSAGE': 'message',
        'MODEL_UPDATED': 'model_updated',
        'MODEL_CREATED': 'model_created',
    }

    def __init__(self, room=None):
        if room is not None:
            self.room = room
        else:
            self.room = 'ws'

    def add_channel(self, reply_channel):
        Group(self.room).add(reply_channel)

    def discard_channel(self, reply_channel):
        Group(self.room).discard(reply_channel)

    def send_message(self, data):
        self.send(data)

    def send(self, data):
        # text = {'event': event, 'data': data}
        stdlogger.info('Send message to ROOM:' +
                       self.room + ' : ' + dumps(data))
        Group(self.room).send({'text': dumps(data)})

    def send_model_updated(self, instance):
        self.send_model(self.EVENTS['MODEL_UPDATED'], instance)

    def send_model_created(self, instance):
        self.send_model(self.EVENTS['MODEL_CREATED'], instance)

    def send_model(self, event, instance):

        # text = {'event': event, 'data': serializers(data).data}
        json = PublishedModelSerializer(instance).data
        text = {'event': event, 'data': json}
        stdlogger.info('Send message to ROOM:' +
                       self.room + ' : ' + dumps(text))
        Group(self.room).send({'text': dumps(text)})


class ChannelPublisher:
    def __init__(self, reply_channel):
        self.reply_channel = reply_channel

    def send(self, json):
        Channel(self.reply_channel).send({'content': dumps(json)})


def ws_model_saved_at(sender=None, *args, **kwargs):

    model_created = kwargs.pop('created')
    instance = kwargs.pop('instance')
    model_name = instance._meta.object_name

    if instance:
        if instance.user_cre:

            key = instance.user_cre.username
            # token, created = Token.objects.get_or_create(
            #    user=instance.user_cre)
            if model_created:
                print('model created')
                GroupPublisher(key).send_model_created(instance)
            else:
                GroupPublisher(key).send_model_updated(instance)
        else:
            stdlogger.warning(
                'user_cre should be present on Model ' + model_name)

    else:
        stdlogger.error(
            'instance is null when calling ws_model_saved_at!! ' + model_name)


def ws_model_deleted_at(sender=None, instance=None, *args, **kwargs):
    print('model deleted')
    pass
