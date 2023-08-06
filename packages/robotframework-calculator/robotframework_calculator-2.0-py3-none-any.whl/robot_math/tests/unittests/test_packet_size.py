import logging
from unittest import TestCase

from robot_math.types import Percent
from robot_math.types.data_packet_type import DataPacket

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(module)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

eq = {
    '8k': '1K',
    '1000K': '1M',
    '8g': '1G',
    '8000k': '1M',
}

summ_p = {
    '2K': ('8k', '1K'),
    '2M': ('1000K', '1M'),
    '2G': ('8g', '1G'),
    '2.1M': ('8000k', '1.1M')
}

summ_n = {
    '2.1M': ('800k', '1M')
}

ne = {
    '8k': '1.1K',
    '1002K': '1M',
    '8.1g': '1G',
    '8020k': '1M',
}


class TestBitrate(TestCase):
    @classmethod
    def setUpClass(cls):
        logging.info(f'{cls.__name__}: Start')

    @classmethod
    def tearDownClass(cls):
        logging.info(f'{cls.__name__}: End')

    def setUp(self):
        logging.info(f'Test {self._testMethodName} start')

    def tearDown(self):
        logging.info(f'Test {self._testMethodName} end')

    def test_bit_value(self):
        b0 = DataPacket(0)
        assert b0 == 0, "Wrong output: {}".format(b0)
        logging.info("Type: {}, Value: {}".format(type(b0).__name__, b0))
        b00 = DataPacket(float(0))
        assert str(b00) == '0.0b', "Wrong output: {}".format(b00)
        logging.info("Type: {}, Value: {}".format(type(b0).__name__, b0))
        b1 = DataPacket('1K')
        assert str(b1) == '1.0K', "Wrong output: {}".format(b1)
        logging.info("Type: {}, Value: {}".format(type(b1).__name__, b1))
        b2 = DataPacket('1M')
        assert str(b2) == '1.0M', "Wrong output: {}".format(b2)
        logging.info("Type: {}, Value: {}".format(type(b2).__name__, b2))
        b3 = DataPacket(number=1, rate='K')
        assert str(b3) == '1.0K', "Wrong output: {}".format(b3)
        logging.info("Type: {}, Value: {}".format(type(b3).__name__, b3))
        b4 = DataPacket('1G')
        assert str(b4) == '1.0G', "Wrong output: {}".format(b4)
        logging.info("Type: {}, Value: {}".format(type(b4).__name__, b4))
        # b4 = PacketSize('1.1G')
        # assert str(b4) == '1.1G', "Wrong output: {}".format(b4)
        # logging.info("Type: {}, Value: {}".format(type(b4), b4))
        b5 = DataPacket('1.1446564G')
        logging.info("Format: {0} vs. {0:.1M}".format(b5))
        # logging.info("Format: {:.2f}".format(b5))

    def test_eq(self):
        for _b1, _b2 in eq.items():
            b1, b2 = DataPacket(_b1), DataPacket(_b2)
            assert b1 == b2, "Wrong output: {} == {}".format(b1, b2)
            logging.info("{} == {}".format(b1, b2))

    def test_ne(self):
        for _b1, _b2 in ne.items():
            b1, b2 = DataPacket(_b1), DataPacket(_b2)
            assert b1 != b2, "Wrong output: {} != {}".format(b1.bit_value, b2.bit_value)
            logging.info("{} != {}".format(b1, b2))

    def test_iadd(self):
        p = DataPacket('1M')
        p_add = DataPacket('1K')
        logging.info(f"{p:.1m}")
        p += p_add
        logging.info(f"{p:.4m}")
        p += '1M'
        logging.info(f"{p:.4m}")

    def test_isub(self):
        p = DataPacket('1M')
        p_sub = DataPacket('1K')
        logging.info(f"{p:.1m}")
        p -= p_sub
        logging.info(f"{p:.4m}")
        p -= '0.1M'
        logging.info(f"{p:.4m}")

    def test_sum_positive(self):
        errors = []
        for _sum, (_b1, _b2) in summ_p.items():
            try:
                s, b1, b2 = DataPacket(_sum), DataPacket(_b1), DataPacket(_b2)
                _b = [b1, b2]
                r_s = sum(_b)
                assert r_s == s, "Wrong output: {} + {} == {} (Actual: {})".format(b1, b2, s, r_s)
                logging.info("{} + {} == {}".format(b1, b2, s))
            except AssertionError as e:
                errors.append(e)
        assert len(errors) == 0, "Following iterations failed:\n{}".format(
            '\n\t'.join([str(e) for e in errors])
        )

    def test_sum_negative(self):
        for _sum, (_b1, _b2) in summ_n.items():
            s, b1, b2 = DataPacket(_sum), DataPacket(_b1), DataPacket(_b2)
            r_s = sum([b1, b2])
            assert r_s != s, "Wrong output: {} + {} == {} (Actual: {})".format(b1, b2, s, r_s)
            logging.info("{} + {} != {} (Actual: {})".format(b1, b2, s, r_s))

    def test_percent(self):
        packet = DataPacket('10M')
        percent = Percent('10%')
        packet += percent
        logging.info(f"{packet}")

    def test_format_conversion(self):
        v = 8000000.8
        p = DataPacket(number=v)
        logging.info(f"{p}")
        logging.info(f"{p:.1b}")
        logging.info(f"{p:.1k}")
        logging.info(f"{p:.2m}")
        logging.info(f"{p:.1B}")
        logging.info(f"{p:.1K}")
        logging.info(f"{p:.1M}")

