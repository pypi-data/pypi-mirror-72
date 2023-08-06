import operator
from abc import ABC, abstractmethod


class _operators(ABC):
    @staticmethod
    @abstractmethod
    def eq(base, other):
        raise NotImplementedError()


LOGICAL_OPERATORS = {
        '__eq__': operator.eq,
        '__ne__': operator.ne,
        '__gt__': operator.gt,
        '__lt__': operator.lt,
        '__ge__': operator.ge,
        '__le__': operator.le,
    }

MATH_OPERATORS = {
    '__add__': operator.add,
    '__iadd__': operator.iadd,
    '__sub__': operator.sub,
    '__isub__': operator.isub,
    '__mul__': operator.mul,
    '__imul__': operator.imul,
    '__idiv__': operator.idiv,
    '__truediv__': operator.truediv,
    '__floordiv__': operator.floordiv
}