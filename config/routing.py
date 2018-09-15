
# channel_routing = {
#     "http.request": "drive.consumers.http_consumer"
# }

from webmarks_bookmarks.channels.consumers import ws_receive
from webmarks_bookmarks.channels.consumers import ws_connect
from webmarks_bookmarks.channels.consumers import ws_disconnect

channel_routing = {
    "websocket.connect": ws_connect,
    "websocket.receive": ws_receive,
    "websocket.disconnect": ws_disconnect,
}
