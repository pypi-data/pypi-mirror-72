from robot_math.types import Percent, TimeInterval
from robot_math.types.data_packet_type import DataPacket


def packet_sum(*packet_list, **kwargs):
    _list = list(packet_list)
    if _list.__len__() == 0:
        return DataPacket(number=0, **kwargs)
    _res = DataPacket(_list.pop())
    while _list.__len__() > 0:
        _next = _list.pop()
        _next.format = _res.rate
        _res += DataPacket(_next, **kwargs)
    return _res


def packet_min(*packet_list, **kwargs):
    _list = list(packet_list)
    if _list.__len__() == 0:
        return DataPacket(number=0, **kwargs)
    _res = DataPacket(_list.pop(), **kwargs)
    while _list.__len__() > 0:
        _next = _list.pop()
        _next.format = _res.rate
        if _next < _res:
            _res = _next
    return _res


def packet_max(*packet_list, **kwargs):
    _list = list(packet_list)
    if _list.__len__() == 0:
        return DataPacket(number=0, **kwargs)
    _res = DataPacket(_list.pop(), **kwargs)
    while _list.__len__() > 0:
        _next = _list.pop()
        _next.format = _res.format
        if _next > _res:
            _res = _next
    return _res


def packet_eq(packet1, packet2, percent):
    return packet1 - percent <= packet2 <= packet1 + percent


def robot_time_eq(time1, time2, percent):
    return time1 - percent <= time2 <= time1 + percent


def float_eq(num1, num2, percent):
    return percent - num1 <= num2 <= percent + num1
