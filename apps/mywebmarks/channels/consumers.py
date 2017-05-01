# coding: utf8
import datetime
import json
import logging
from apps.mywebmarks.channels.publishers import GroupPublisher
from apps.mywebmarks.channels.publishers import Message
from channels.handler import AsgiHandler
from channels.sessions import channel_session
from django.http import HttpResponse
# from pprint import pprint

stdlogger = logging.getLogger(__name__)


def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse(
        "Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


def get_room(message):
    # {'text': message.content['query_string']
    path = message.content['path']
    return path.strip("/").split("/")[-1]


@channel_session
def ws_receive(message):
    print(' Server received websocket data.' + str(datetime.datetime.now()))
    room = get_room(message)
    # print(message.content['query_string'])
    text = message.content.get('text')
    j = json.loads(text)
    print(text)
    GroupPublisher(room).send_message(j)


@channel_session
def ws_connect(message):
    room = get_room(message)
    stdlogger.info(' Server ws_connect received websocket from user ' +
                   room + ' at ' + str(datetime.datetime.now()))

    message.reply_channel.send({'accept': True})

    publisher = GroupPublisher(room)
    publisher.add_channel(message.reply_channel)
    publisher.send_message(Message(room + ' login from host ').as_dict())


@channel_session
def ws_disconnect(message):
    room = get_room(message)
    stdlogger.info(' Server ws_disconnect received websocket from user ' +
                   room + ' at ' + str(datetime.datetime.now()))

    GroupPublisher(room).discard_channel(message.reply_channel)
