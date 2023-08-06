import re
from abc import ABC, abstractmethod


class _SpecialType(ABC, type):

    FORMAT_PARSE_REGEX = re.compile(r'^\.([\d]+)([a-zA-Z%]?)$')

    def __new__(mcs, *args, **kwargs):
        return super().__new__(mcs, mcs.__name__, (object,), kwargs)

    def __init__(cls, units_count, **kwargs):
        super().__init__(cls.__name__)
        cls.__repr__ = cls.__str__
        try:
            cls._unit_type = kwargs.get('type', float)
            cls._units = cls._unit_type(units_count)
            assert isinstance(cls._units, cls._unit_type)
            _unit_name = kwargs.get('units', 'units')
            if _unit_name != 'units':
                setattr(cls, _unit_name, cls.units)

        except Exception:
            raise ValueError(f"Value must be numeric only vs. {units_count} - ({type(units_count).__name__})")

    def __float__(self):
        return float(self.units)

    def __int__(self):
        return int(self.units)

    def _get_round_from_format_spec(cls, format_spec, adjust=False):
        m = cls.FORMAT_PARSE_REGEX.match(format_spec)
        if m is None:
            raise ValueError(f"Wrong format: {format_spec}")
        _spec_index, _spec_char = int(m.groups()[0]), m.groups()[1]

        if adjust:
            _in_str = str(cls.units / 100).split('.', 2)[1]
            _spec_index = len(_in_str)
        return _spec_index, _spec_char

    @property
    def units(self):
        return self._unit_type(self._units)

    def cast_to_units(self, value, **kwargs) -> float:
        if type(self) != type(value):
            return self._unit_type(self.from_units(value, **kwargs))
        return value.units

    @abstractmethod
    def __str__(self):
        raise NotImplementedError()

    def __repr__(self):
        return str(self)

    @staticmethod
    @abstractmethod
    def from_units(value, **kwargs):
        raise NotImplementedError()

    def __eq__(self, other):
        return self.units == self.cast_to_units(other)

    def __ne__(self, other):
        return not _SpecialType.__eq__(self, other)

    def __gt__(self, other):
        return self.units > self.cast_to_units(other)

    def __lt__(self, other):
        return self.units < self.cast_to_units(other)

    def __ge__(self, other):
        return self.units >= self.cast_to_units(other)

    def __le__(self, other):
        return self.units <= self.cast_to_units(other)

    def __add__(self, other):
        return self.from_units(self.units + self.cast_to_units(other))

    def __iadd__(self, other):
        self._units = self._units + self.cast_to_units(other)
        return self

    def __sub__(self, other):
        return self.from_units(self.units - self.cast_to_units(other))

    def __isub__(self, other):
        self._units = self._units - self.cast_to_units(other)
        return self

    def __idiv__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Dividing allowed to numbers only")
        return self.from_units(self.units / self.cast_to_units(other))

    def __mul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Multiplexing allowed to numbers only")
        self._units = self._units * other
        return self

    def __imul__(self, other):
        if not isinstance(other, (int, float)):
            raise TypeError("Multiplexing allowed to numbers only")
        self._units = self.units / other
        return self

    def __truediv__(self, other):
        return _SpecialType.__idiv__(self, other)

    def __floordiv__(self, other):
        return _SpecialType.__idiv__(self, other)
