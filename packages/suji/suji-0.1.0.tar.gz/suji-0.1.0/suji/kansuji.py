""" The entry point to the kansuji methods.

This provides a method to convert from the mixed japanese number notation to Kansuji string value,
and a method to convert from mixed number notations to Kansuji string.
"""
from suji.converter import values


class Kansuji:

    __zero = '零'

    __minus = 'マイナス'

    __number = {
        1: '一',
        2: '二',
        3: '三',
        4: '四',
        5: '五',
        6: '六',
        7: '七',
        8: '八',
        9: '九',
    }

    __radic = [
        10000000000000000,
        1000000000000,
        100000000,
        10000,
        1000,
        100,
        10,
    ]

    __radic_kanji = [
        '京',
        '兆',
        '億',
        '万',
        '千',
        '百',
        '十',
    ]

   # __before_the_decimal_point = '割'

   # __radic_adp = [
   #     0.1,
   #     0.01,
   #     0.001,
   # ]

   # __radic_adp_kanji = [
   #     '分',
   #     '厘',
   #     '毛',
   # ]
        
    @staticmethod
    def __value(v, index, one):
        if v == 0:
            return ''
        if v < 0:
            return Kansuji.__minus + Kansuji.__value(-1 * v, index, one)
        if v in Kansuji.__number:
            return Kansuji.__number[v]
        if len(Kansuji.__radic) <= index:
            if v in Kansuji.__number:
                return Kansuji.__number[v]
            else:
                return ''

        nd = divmod(v, Kansuji.__radic[index])
        if nd[0] == 0:
            return Kansuji.__value(v, index + 1, one)

        prefix = ''
        if nd[0] != 1:
            prefix = Kansuji.__value(nd[0], index + 1, one)
        elif one:
            prefix = Kansuji.__number[1]

        return prefix \
            + Kansuji.__radic_kanji[index] \
            + Kansuji.__value(nd[1], index + 1, one)

    @staticmethod
    def value(v, one=True):
        v = int(v)
        if v == 0:
            return Kansuji.__zero
        return Kansuji.__value(v, 0, one)
    
    
def kansujis(src, one=True):
    """ Convert from mixed Japanese number notations to Knasuji string values.
    The return value is a list of Kansuji value objects.
    If the input string has no number notation, `kansujis` returns a empty list.

    The result object has three keys: `val`, `beg`, and `end`:

    :val: the string value of the Kansuji notation.
    :beg: the start postion of the found number notation at the input string.
    :end: the end postion of the found number notation.

    :param src: a input string.
    :param one: a boolean flag for the display `ichi`. Default is True.
    :return: a list of the Kansuji value objects.
    """
    val = values(src)
    for v in val:
        v['val'] = Kansuji.value(v['val'], one)
    return val


def kansuji(src, one=True):
    """ Convert from mixed number notations to Kansuji string.
    The return value is a converted str.
    If the input string has no number notation, `kansuji` returns the input str.

    :param src: a input string.
    :param one: a boolean flag for the display `ichi`. Default is True.
    :return: a converted str.
    """
    vals = values(src)
    if 0 == len(vals):
        return src

    start = 0
    s = ''
    for v in vals:
        s += src[start:v['beg']]
        s += Kansuji.value(v['val'], one)
        start = v['end']
    s += src[start:len(src)]
    return s


__all__ = ['kansujis', 'kansuji']
