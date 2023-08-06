import socket
import struct


class ProtocolDecoder(object):

    def __init__(self):
        self._buffer = []
        self._completed = False

    def completed(self):
            return self.header_complete() and (len(self._buffer) - 4) == self.len()

    def tag(self):
        return struct.unpack('!h', bytes(self._buffer[:2]))[0]

    def len(self):
        try:
            return struct.unpack('!h', bytes(self._buffer[2:4]))[0]
        except struct.error as e:
            raise e

    def header_complete(self):
        return len(self._buffer) >= 4

    def read(self, data):
        return self._buffer.extend(data)

    def data(self):
        return bytes(self._buffer[4:])


class ProtocolBuilder(object):

    def __init__(self, tag):
        self._tag = tag
        self._buffer = []
        self.add_short(tag)
        self.add_short(0)

    def _update_len(self):
        new_len = struct.pack('!H', len(self._buffer)-4);
        self._buffer[2] = new_len[0]
        self._buffer[3] = new_len[1]

    def add_bool(self, value):
        self._buffer.extend(struct.pack('c', b"\0" if not value else b"\1"))

    def add_byte(self, value):
        self._buffer.extend(struct.pack('c', bytes([value])))

    def add_char(self, c):
        self._buffer.append(bytes([c]))

    def add_short(self, s):
        self._buffer.extend(struct.pack('!h', int(s)))

    def add_long(self, s):
        self._buffer.extend(struct.pack('!l', int(s)))

    def add_ushort(self, s):
        self._buffer.extend(struct.pack('!H', int(s)))

    def add_ulong(self, s):
        self._buffer.extend(struct.pack('!L', int(s)))

    def build(self):
        self._update_len()
        return  bytes(self._buffer)

