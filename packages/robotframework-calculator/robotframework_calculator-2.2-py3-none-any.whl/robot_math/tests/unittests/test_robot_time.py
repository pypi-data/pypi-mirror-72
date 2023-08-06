import logging
from unittest import TestCase
import operator
from robot_math.types import TimeInterval
from robot_math.types.percent_type import Percent


class TestRobotTimeInterval(TestCase):

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
        err = {}
        for pattern in ['3d2h45m20s', 1, 2.1, '1', '2.4', '2s', '2m', '3.5h']:
            try:
                item = TimeInterval(pattern)
            except Exception as e:
                err.update({pattern: e})
            else:
                logging.info(f"{pattern}: {item}")

        assert len(err) == 0, "Errors:\n{}".format('\n'.join([f"{k}: {v}" for k, v in err.items()]))

    def test_02(self):
        err = {}
        for num1, num2 in [(TimeInterval('1h'), TimeInterval('20s')),
                           (TimeInterval('1h'), TimeInterval('22s')),
                           (TimeInterval('1h'), TimeInterval('60m')),
                           (TimeInterval('1h'), 3),
                           (TimeInterval('1h'), TimeInterval(3))
                           ]:
            logging.info(f'--{num1}, {num2}-----------------')
            for op in (operator.eq, operator.ne, operator.add, operator.sub):
                try:
                    logging.info(f"\t{op.__name__}({num1}, {num2}) = {op(num1, num2)}")
                except Exception as e:
                    err.update({f"{op.__name__}({num1}, {num2})": e})

            logging.info('----------------------------')
        assert len(err) == 0, "Errors:\n{}".format('\n'.join([f"{k}: {v}" for k, v in err.items()]))

    def test_03(self):
        err = {}
        for num1, num2 in [(TimeInterval('1h'), 2),
                           (TimeInterval('1h'), 4),
                           (TimeInterval('1h'), 2.5),
                           (TimeInterval('1h'), 3),
                           ]:
            for op in (operator.mul, operator.truediv):
                try:
                    logging.info(f"\t{op.__name__}({num1}, {num2}) = {op(num1, num2)}")
                except Exception as e:
                    err.update({f"{op.__name__}({num1}, {num2})": e})

            logging.info('----------------------------')
        assert len(err) == 0, "Errors:\n{}".format('\n'.join([f"{k}: {v}" for k, v in err.items()]))

    def test_robottime_persent(self):
        t1 = TimeInterval('1d')
        p = Percent('10%')
        logging.info(f"Orig time in d: {t1:d}: {t1 + p:d}")
        logging.info(f"Orig time in h: {t1:h}: {t1 + p:h}")
        logging.info(f"Orig time in m: {t1:m}: {t1 + p:m}")
        logging.info(f"Orig time in s: {t1:s}: {t1 + p:s}")
        t1 += p
        logging.info(f"New time: {t1:h}")
