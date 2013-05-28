import logging

from socketio.namespace import BaseNamespace
#from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.mixins import BroadcastMixin
from socketio.sdjango import namespace


class LonelyRoomMixin(object):
    def __init__(self, *args, **kwargs):
        super(LonelyRoomMixin, self).__init__(*args, **kwargs)
        if 'rooms' not in self.session:
            self.session['rooms'] = set()  # a set of simple strings

    def join(self, room):
        """Lets a user join a room on a specific Namespace."""
        self.session['rooms'].add(self._get_room_name(room))

    def leave(self, room):
        """Lets a user leave a room on a specific Namespace."""
        self.session['rooms'].remove(self._get_room_name(room))

    def _get_room_name(self, room):
        return self.ns_name + '_' + room

    def emit_to_room(self, room, event, *args):
        """This is sent to all in the room (in this particular Namespace)"""
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)
        room_name = self._get_room_name(room)
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'rooms' not in socket.session:
                continue
            #if room_name in socket.session['rooms'] and self.socket != socket:
            if room_name in socket.session['rooms']:
                socket.send_packet(pkt)


@namespace('/chat')
class ChatNamespace(BaseNamespace, LonelyRoomMixin, BroadcastMixin):
    nicknames = []

    def initialize(self):
        self.logger = logging.getLogger("socketio.chat")
        self.log("Socketio session started")

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))

    def on_join(self, room):
        self.room = room
        self.join(room)
        return True

    def on_nickname(self, nickname):
        print("Creating the nickname: " + nickname)
        self.log('Nickname: {0}'.format(nickname))
        self.socket.session['nickname'] = nickname
        self.nicknames.append(nickname)
        self.broadcast_event('announcement', '%s has connected' % nickname)
        self.broadcast_event('nicknames', self.nicknames)
        return True, nickname

    def recv_disconnect(self):
        self.log('Disconnected')
        nickname = self.socket.session['nickname']
        self.nicknames.remove(nickname)
        self.broadcast_event('announcement', '%s has disconnected' % nickname)
        self.broadcast_event('nicknames', self.nicknames)
        self.disconnect(silent=True)
        return True

    def on_user_message(self, msg):
        self.log('User message: {0}'.format(msg))
        # TODO: dig into the logic of emit_to_room
        self.emit_to_room(self.room, 'msg_to_room',
                          self.socket.session['nickname'], msg)
        return True
