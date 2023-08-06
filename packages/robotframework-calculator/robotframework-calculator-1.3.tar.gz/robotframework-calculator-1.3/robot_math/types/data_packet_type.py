
import enum
import re

from .abstracts import TypeAbstract
from . import Percent

BIT = 1
BYTE = 8
KILO = 1000


class PacketUnit(enum.IntEnum):
    b = BIT
    B = BYTE
    k = KILO
    K = KILO * BYTE
    m = pow(KILO, 2)
    M = pow(KILO, 2) * BYTE
    g = pow(KILO, 3)
    G = pow(KILO, 3) * BYTE


BITRATE_REGEX = re.compile(r'([\d.]+)(.*)')


class DataPacket(TypeAbstract):
    def __init__(cls, value_str=None, **kwargs):
        try:
            value_str = '0' if value_str == 0 else value_str
            rate = kwargs.get('rate', '')
            if rate != '':
                rate = cls._get_rate(rate).name
            parsing_value = value_str or f"{kwargs.get('number', '')}{rate}"
            if parsing_value == '':
                raise ValueError(f"Packet size not provided: neither in '{value_str}' or '{kwargs}")
            number, rate_name = cls.parse(parsing_value)
            cls.rate = PacketUnit[rate_name if rate == '' else rate]
            super().__init__(int(number * cls._rate), type=int, units='bits')
        except Exception as e:
            raise ValueError(f"Cannot parse string '{e}'")

    @staticmethod
    def _get_rate(rate):
        if isinstance(rate, PacketUnit):
            return rate
        else:
            return PacketUnit[rate]

    @property
    def rate(cls):
        return cls._rate

    @rate.setter
    def rate(cls, rate):
        cls._rate = cls._get_rate(rate)

    def _to_string(cls, format_spec, rate=None):
        rate = PacketUnit[rate] if rate else cls._rate
        return f"{cls.units / rate:{format_spec}}{rate.name}"

    @staticmethod
    def parse(bitrate_str: str):
        try:
            m = BITRATE_REGEX.match(str(bitrate_str))
            if m is None:
                raise AttributeError("Wrong bitrate format ({})".format(bitrate_str))
            number = float(m.groups()[0])
            rate = m.groups()[1] or PacketUnit.b.name
            return number, rate
        except Exception as e:
            raise type(e)("Cannot parse PacketSize value string '{}' with error: {}".format(bitrate_str, e))

    @staticmethod
    def from_units(value, rate=PacketUnit.b):
        if isinstance(value, str):
            return DataPacket(value, rate=rate)
        return DataPacket(number=value / rate, rate=rate)

    def __format__(self, format_spec):
        rates = [r for r in list(PacketUnit) if format_spec.endswith(r.name)]
        if len(rates) == 1:
            rate = rates[0].name
            format_spec = format_spec.replace(rate, 'f')
            return self._to_string(format_spec, rate=rate)
        elif len(rates) == 0:
            return self._to_string(format_spec)
        else:
            raise IndexError()

    def __str__(self):
        return self._to_string('')

    def __radd__(self, other):
        if other == 0:
            return self
        else:
            return self + other

    def __add__(self, other):
        if type(other) == Percent:
            return self.from_units(other + self.units, rate=self.rate)
        return self.from_units(other + self.units, rate=self.rate)

    def __iadd__(self, other):
        if type(other) == Percent:
            self._units = self.from_units(other + self.units, rate=self.rate)
            return self
        return super().__iadd__(other)

    def __sub__(self, other):
        if type(other) == Percent:
            return self.from_units(other - self.units, rate=self.rate)
        return super().__sub__(other)

    def __isub__(self, other):
        if type(other) == Percent:
            self._units = other - self.units
            return self
        return super().__isub__(other)
