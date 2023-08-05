""" An accumulator for japanese number notation.
"""


class Acc:

    def __init__(self):
        self.inside = False
        self.__beg = None
        self.__end = None
        self.__val = 0
        self.__val_cardinal = 0
        self.__last_cardinal = 10
        self.__oku = 0
        self.__base = 10

    def dump(self):
        s = 'Acc:'
        s += '\tinside: '          + str(self.inside)
        s += '\t__beg: '           + str(self.__beg)
        s += '\t__end: '           + str(self.__end)
        s += '\t__val: '           + str(self.__val)
        s += '\t__val_cardinal: '  + str(self.__val_cardinal)
        s += '\t__last_cardinal: ' + str(self.__last_cardinal)
        s += '\t__oku: '           + str(self.__oku)
        s += '\t__base: '          + str(self.__base)
        print(s)

    def index_increment(self, index):
        if not self.inside:
            return
        if self.__beg is None:
            self.__beg = index
            self.__end = index + 1
            return
        self.__end += 1

    def turn_to_decimal_state(self, index):
        if not self.inside:
            self.inside = True
        self.index_increment(index)
        self.__val = float(self.__val)
        self.__val_cardinal = float(self.__val_cardinal)
        self.__base = float(0.1)

    def attach_cardinal(self, index, cardinal):
        self.inside = True
        self.index_increment(index)

        val = 1 if self.__val == 0 else self.__val

        if self.__last_cardinal < cardinal:
            if self.__val == 0 and self.__val_cardinal != 0:
                self.__val_cardinal = self.__val_cardinal * cardinal
            else:
                self.__val_cardinal = (self.__val_cardinal + val) * cardinal
            self.__val = 0
        else:
            self.__val_cardinal = self.__val_cardinal + (val * cardinal)

        if 100000000 <= self.__val_cardinal:
            self.__oku += self.__val_cardinal
            self.__val_cardinal = 0

        self.__last_cardinal = cardinal
        self.__val = 0

    def attach_number(self, index, number):
        self.inside = True
        self.index_increment(index)
        if self.__base < 1:
            self.__val = self.__val  + (float(number) * self.__base)
            self.__base *= 0.1
        else:
            self.__val = (self.__val * self.__base) + number

    def get_value(self):
        return {
            'val': self.__oku + self.__val_cardinal + self.__val,
            'beg': self.__beg,
            'end': self.__end,
        }
