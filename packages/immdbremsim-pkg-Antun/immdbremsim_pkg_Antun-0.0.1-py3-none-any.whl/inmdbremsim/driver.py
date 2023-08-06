import socket
import utils
import struct
import messages


class Driver(object):

    def __init__(self, ip, port=11000):
        self._is_open = False
        self._ip = ip
        self._port = port
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __enter__(self):
        if not self._is_open:
            self._socket.connect((self._ip, self._port))
            self._is_open = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._is_open:
            self._socket.close()
            self._is_open = False


    def __read_status_message(self):
        decoder = utils.ProtocolDecoder()
        buf = bytes()
        while len(buf) != 4:
            missing = 4 - len(buf)
            tmpbuf = self._socket.recv(missing, socket.MSG_WAITALL)
            buf = buf + tmpbuf

        while not decoder.completed():
            decoder.read(buf)
            buf = self._socket.recv(decoder.len())

        if(decoder.tag() == 1):
            return messages.StatusMessage(True, "")
        elif decoder.tag() == 3:
            return messages.StatusMessage(False, str(decoder.data()))
        else:
            return messages.StatusMessage(False, "")


    def get_device_status(self):
        builder = utils.ProtocolBuilder(6)
        self._socket.send(builder.build())
        buf = self._socket.recv(12)
        decoder = utils.ProtocolDecoder()
        while not decoder.completed():
            decoder.read(buf)
        return messages.DeviceStatuses(struct.unpack('cccccccc', decoder.data()))

    def check_alive(self):
        builder = utils.ProtocolBuilder(1)
        self._socket.send(builder.build())
        return self.__read_status_message()

    def reset_all_devices(self):
        builder = utils.ProtocolBuilder(8)
        self._socket.send(builder.build())
        return self.__read_status_message()

    def deposit_coin_and_perform_vend(self, selection, selection_value, coin_type):
        builder = utils.ProtocolBuilder(9)
        builder.add_byte(selection)
        builder.add_short(selection_value)
        builder.add_byte(coin_type)
        self._socket.send(builder.build())
        return self.__read_status_message()

    def begin_session_and_perform_vend(self, credit, product_price, selection):
        builder = utils.ProtocolBuilder(11)
        builder.add_ushort(credit)
        builder.add_ushort(product_price)
        builder.add_ushort(selection)
        self._socket.send(builder.build())
        return self.__read_status_message()

    def cc_report_event(self, event):
        builder = utils.ProtocolBuilder(10)
        builder.add_byte(event)
        self._socket.send(builder.build())
        return self.__read_status_message()

    def power_reset(self):
        builder = utils.ProtocolBuilder(12)
        self._socket.send(builder.build())
        return self.__read_status_message()


