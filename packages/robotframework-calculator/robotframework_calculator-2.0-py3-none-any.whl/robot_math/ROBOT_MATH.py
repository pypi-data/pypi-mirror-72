import operator
import re

from robot.api import logger
from robot.api.deco import keyword
from robot.errors import FrameworkError

from robot_math import __version__ as version
from robot_math.types.cross_type_operators import packet_eq, robot_time_eq, float_eq
from robot_math.types import Percent, DataPacket, TimeInterval, format_factory, type_factory

__version__ = version

__doc__ = """Providing KW allowing operation with percent, packet, robot_math time as regular numbers
    
"""

__all__ = [
    'list_sum',
    'packet_operation',
    'time_operation',
    'numeric_operation',
    'get_packet',
    'get_time_interval'
]


@keyword("LIST_SUM")
def list_sum(*argv, **kwargs):
    """
    Summarise items in provided list

    Arguments:
    - argv: list of item for summarise

    Options:
        - type: list item type (int if omitted)

    Returns sum number in 'type' format

    """
    _type = kwargs.get('type', int)
    _result: _type = 0
    try:
        for _list in argv:
            if isinstance(_list, (list, tuple)):
                _result += sum([_type(_item) for _item in _list])
            else:
                _number = _type(_list)
                _result += _number
    except (ValueError, IndexError) as e:
        raise FrameworkError(f"ROBOT_MATH.LIST_SUM: {e}")
    else:
        return _result


def _robot_time_operation(operation):
    if operation in ['eq', '=', '==']:
        return operator.eq
    elif operation in ['ne', '!=', '<>']:
        return operator.ne
    elif operation in ['gt', '>']:
        return operator.gt
    elif operation in ['ge', '>=']:
        return operator.ge
    elif operation in ['lt', '<']:
        return operator.lt
    elif operation in ['le', '<=']:
        return operator.le
    elif operation in ['add', '+']:
        return operator.add
    # elif operation in ['iadd', '+=']:
    #     return operator.iadd
    elif operation in ['sub', '-']:
        return operator.sub
    # elif operation in ['isub', '-=']:
    #     return operator.isub
    elif operation in ['div', '/']:
        return operator.truediv
    # elif operation in ['idiv', '/=']:
    #     return operator.itruediv
    elif operation in ['mul', '*']:
        return operator.mul
    # elif operation in ['imul', '*=']:
    #     return operator.imul
    else:
        raise ValueError(f"Operator '{operation}' not valid")


def _parse_line(expression, *extra_types):
    regex_exp = r'(\d\w+)\s*([\+\-\*\/\=<>]{,2})\s*(.+)'
    regex = re.compile(regex_exp)
    m = regex.match(expression)
    assert m is not None, f"Expression {expression} not math"
    assert len(m.groups()) == 3, f"Wrong expression {expression}"
    operand1 = format_factory(m.groups()[0], *extra_types)
    operation = _robot_time_operation(m.groups()[1])
    operand2 = format_factory(m.groups()[2], *extra_types)
    return operand1, operation, operand2


def _type_evaluation(**kwargs):
    operand1 = kwargs.get('operand1', None)
    operand2 = kwargs.get('operand2', None)
    operation = kwargs.get('operation', None)
    deviation = kwargs.get('deviation', None)
    special_eq = kwargs.get('special_eq')
    logger.trace(f"{operand1} {operation.__name__} {operand2}{f' (Deviation: {deviation}' if deviation else ''})")
    if deviation:
        assert not all(type(operand) == Percent for operand in [operand2, deviation]), \
            f"Operation between Packet and Percent doesn't allow deviation"
    if deviation and operation == operator.eq:
        result = special_eq(operand1, operand2, deviation)
    else:
        if isinstance(operand1, (float, int)):
            result = operation(operand2, operand1)
        else:
            result = operation(operand1, operand2)
    logger.debug(f"Result: {result}")
    return result


@keyword("PACKET_OPERATION")
def packet_operation(expression_str, deviation_str=None, reason=None):
    """
    Provide logical and mathematical operation with packet

    - expression_str: operand1 operation operand2

    | Example | Comments |
    | 1M * 2 | Multiple Packet size 2M |
    | 1M + 10K | Return packet size 1.01M |
    | 1M + 10% | Return packet size 1.1M |

    Options:
    - deviation: add on for comparison verifications (eq, ,gt, lt, ge, le)

    Equality Examples:

    | Operand1  Operation  Operand2 | Deviation   | Result    | Comments  |
    | 10M  == 12M                   | 25%       | TRUE      | (10M - 25%) < 12M < (10M + 25%)   |
    | 10M  == 12M                   | 0.25       | TRUE      | (10M - 25%) < 12M < (10M + 25%)   |
    | 10M  == 12M                   | -25%       | FALSE      | (10M - 25%) < 12M < 10M   |
    | 10M  == 12M                   | +25%      | TRUE      | 10M < 12M < (10M + 25%)   |

    - reason: Custom fail reason

    return: TRUE/FALSE for logical operation and value for math operation
    """
    try:

        logger.trace(f"{expression_str}{', ' + deviation_str  if deviation_str else ''}")
        _deviation = format_factory(deviation_str, Percent) if deviation_str else None
        operand1, operation, operand2 = _parse_line(expression_str, DataPacket, Percent)
        result = _type_evaluation(operand1=operand1, operand2=operand2,
                                  operation=operation, deviation=_deviation, special_eq=packet_eq)
        assert result is not False, f"{operand1} {operation.__name__} {operand2} False" if reason is None else reason
        return result
    except AssertionError as e:
        raise e
    except Exception as e:
        raise FrameworkError(e)


@keyword("TIME_OPERATION")
def time_operation(expression_str, deviation_str=None, reason=None):
    """
        RF_MATH_OPERATION

        - expression: operand1 operation operand2

        | Example | Comments |
        | 1h * 3 | Return 3h |
        | 1h + 10% | Return 1h 6m |

    - deviation: add on for comparison verifications (eq, ,gt, lt, ge, le)

        Equality Examples:
            | Operand1  | Operand2  | Percent   | Result    | Comments  |
            | 10m       | 12m       | 25%       | TRUE      | 10m - 25% < 12m < 10m + 25%   |
            | 10m       | 12m       | -25%       | FALSE      | 10m - 25% < 12m < 10m   |
            | 10m       | 12m       | +25%       | TRUE      | 10m < 12m < 10m + 25%   |

    - reason: Custom fail reason

        return: TRUE/FALSE for logical operation and value for math operation
        """
    try:
        logger.trace(f"{expression_str}{', ' + deviation_str if deviation_str else ''}")
        _deviation = format_factory(deviation_str, Percent) if deviation_str else None
        operand1, operation, operand2 = _parse_line(expression_str, float, TimeInterval, Percent)
        result = _type_evaluation(operand1=operand1, operand2=operand2,
                                  operation=operation, deviation=_deviation, special_eq=robot_time_eq)
        assert result is not False, f"{operand1} {operation.__name__} {operand2} False" if reason is None else reason
        return result
    except AssertionError as e:
        raise e
    except Exception as e:
        raise FrameworkError(e)


@keyword("NUMERIC_OPERATION")
def numeric_operation(expression_str, deviation_str=None, reason=None):
    """
        Provide logical and mathematical operation with packet

        - expression_str: operand1 operation operand2

        | Example | Comments |
        | 1M * 2 | Multiple Packet size 2M |
        | 1M + 10K | Return packet size 1.01M |
        | 1M + 10% | Return packet size 1.1M |

        Options:
        - deviation: add on for comparison verifications (eq, ,gt, lt, ge, le)

        Equality Examples:

        | Operand1  Operation  Operand2 | Deviation   | Result    | Comments  |
        | 10M  == 12M                   | 25%       | TRUE      | (10M - 25%) < 12M < (10M + 25%)   |
        | 10M  == 12M                   | 0.25       | TRUE      | (10M - 25%) < 12M < (10M + 25%)   |
        | 10M  == 12M                   | -25%       | FALSE      | (10M - 25%) < 12M < 10M   |
        | 10M  == 12M                   | +25%      | TRUE      | 10M < 12M < (10M + 25%)   |

        - reason: Custom fail reason

        return: TRUE/FALSE for logical operation and value for math operation
        """
    try:

        logger.trace(f"{expression_str}{', ' + deviation_str if deviation_str else ''}")
        _deviation = format_factory(deviation_str, Percent) if deviation_str else None
        operand1, operation, operand2 = _parse_line(expression_str, float, Percent)
        result = _type_evaluation(operand1=operand1, operand2=operand2,
                                  operation=operation, deviation=_deviation, special_eq=float_eq)
        assert result is not False, f"{operand1} {operation.__name__} {operand2} False" if reason is None else reason
        return result
    except AssertionError as e:
        raise e
    except Exception as e:
        raise FrameworkError(e)


@keyword("GET_PACKET")
def get_packet(packet_str):
    """
    GET_PACKET
    Converting packet string to numeric object
    - time_str: Packet string in iperf format (1M, 1m, 2K, 5T, 1000b, 12B, etc)
    - return: Packet object
    """
    return DataPacket(packet_str)


@keyword("GET_TIME_INTERVAL")
def get_time_interval(time_str):
    """
    GET_TIME_INTERVAL
    Converting time string to numeric object
    - time_str: Time string in robot format (3h, 1h 20m 3s, etc)
    - return: TimeInterval object
    """
    return TimeInterval(time_str)
