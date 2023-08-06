import unittest
import utils
import struct
import driver

class ProtocolTest(unittest.TestCase):

    def connect(self):
        drv = driver.Driver("10.10.20.124", 11000)
        return drv


    def testDecoder(self):
        decoder = utils.ProtocolDecoder()
        self.assertFalse(decoder.completed())
        decoder.read(b"\0")
        self.assertFalse(decoder.completed())
        decoder.read(b"\0")
        self.assertFalse(decoder.completed())
        decoder.read(b"\0")
        self.assertFalse(decoder.completed())
        decoder.read(b"\0")
        self.assertTrue(decoder.completed())
        self.assertEqual(decoder.tag(), 0)
        self.assertEqual(decoder.len(), 0)

    def testDecoderShort(self):
        decoder = utils.ProtocolDecoder()
        self.assertFalse(decoder.completed())
        decoder.read(b"\0\1\0\2\0\1")
        self.assertTrue(decoder.completed())
        self.assertEqual(decoder.tag(), 1)
        self.assertEqual(decoder.len(), 2)
        self.assertEqual(struct.unpack('!h', decoder.data())[0], 1)

    def testDecoderLong(self):
        decoder = utils.ProtocolDecoder()
        self.assertFalse(decoder.completed())
        decoder.read(b"\0\2\0\4\0\1\2\3")
        self.assertTrue(decoder.completed())
        self.assertEqual(decoder.tag(), 2)
        self.assertEqual(decoder.len(), 4)
        self.assertEqual(struct.unpack('!l', decoder.data())[0], 0x010203)

    def test_driver(self):
        with self.connect() as drv:
            self.assertTrue(drv.check_alive())

    def test_driver_loop_10(self):
        for _ in range(0, 10):
            with self.connect() as drv:
                self.assertTrue(drv.check_alive())

    def test_reset_all_devices(self):
        with self.connect() as drv:
            self.assertTrue(drv.reset_all_devices())

    def test_driver_status(self):
        with self.connect() as drv:
            status = drv.get_device_status()
            self.assertTrue(status.cc)
            self.assertTrue(status.cl1)
            self.assertTrue(status.vmc_cl1_ready)
            self.assertTrue(status.vmc_cc_ready)

    def test_deposit_coin_and_perform_vend(self):
        with self.connect() as drv:
            status = drv.deposit_coin_and_perform_vend(2, 100, 3)
            print(status.msg)
            self.assertTrue(status.ok)

    def test_begin_session_and_perform_vend(self):
        with self.connect() as drv:
            status = drv.begin_session_and_perform_vend(1000, 500, 1)
            print(status.msg)
            self.assertTrue(status.ok)

    def test_cc_event(self):
        with self.connect() as drv:
            status = drv.cc_report_event(4)
            print(status.msg)
            self.assertTrue(status.ok)

    def test_power_reset(self):
        with self.connect() as drv:
            status = drv.power_reset()
            print(status.msg)
            self.assertTrue(status.ok)

    def test_send_5_cc_vends_sequentially(self):
        for _ in range(0, 5):
            with self.connect() as drv:
                status = drv.deposit_coin_and_perform_vend(2, 100, 3)
                self.assertTrue(status.ok)

    def test_send_5_cashless_vends(self):
        for _ in range(0, 5): 
            with self.connect() as drv:
                status = drv.begin_session_and_perform_vend(1000, 500, 1)
                print(status.msg)
                self.assertTrue(status.ok)
