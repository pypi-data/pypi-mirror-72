from unittest import TestCase
from robot_math.types import Percent
import logging


class TestPercent(TestCase):
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

    def test_01(self):
        p1 = Percent('10%', 4)
        logging.info("{:.2%}".format(p1))
        n1 = 10006
        logging.info(f"{n1:02d}")
        logging.info(f"{p1 + n1}")
        logging.info(f"{p1 - n1}")

    def test_02(self):
        p1 = Percent(10.5)
        logging.info(f"{repr(p1)}")
        logging.info(f"{p1}")
        logging.info(f"{p1:.1%}")
        logging.info(f"{p1:.0%}")
        logging.info(f"{p1:.4f}")
        logging.info(f"{p1:.2f}")
        n1 = 10006
        logging.info(f"{n1}")

        expected = n1 * (100 + 10.5)/100
        assert p1 + n1 == expected, f"Expected ({expected}) vs {p1-n1}"
        logging.info(f"{p1 + n1} - {expected}")
        expected = n1 * (100 - 10.5) / 100
        assert p1 - n1 == expected, f"Expected ({expected}) vs {p1-n1}"
        logging.info(f"{p1 - n1} - {expected}")

    def test_03(self):
        p1 = Percent('-10.5')
        n1 = 10006
        logging.info(f"{n1}")
        high_expected = n1
        assert p1 + n1 == high_expected, f"Expected ({high_expected}) vs {p1+n1}"
        logging.info(f"{p1 + n1} - {high_expected}")
        low_expected = n1 * (100 - 10.5) / 100
        assert p1 - n1 == low_expected, f"Expected ({low_expected}) vs {p1-n1}"
        logging.info(f"{p1 - n1} - {low_expected}")

    def test_04_in_range(self):
        err = []
        for n1, n2, p_1, exp in [(100, 110, '10%', True),
                                 (100, 90, '10%', True),
                                 (100, 101, '-10%', False),
                                 (100, 90, '+10%', False),
                                 (100, 99.5, '0.5%', True),
                                 (100, 50, '0.5', True)]:
            try:
                p1 = Percent(p_1)
                assert p1.in_range(n1, n2), f"Number {n2} not in range with {n1} for {p1}"
                logging.info(f"Number {n2} is in range with {n1} for {p1}")
            except Exception as e:
                if not exp:
                    logging.info(e)
                else:
                    err.append(e)
        assert len(err) == 0, f"Errors: {err}"
        logging.info('Pass')
