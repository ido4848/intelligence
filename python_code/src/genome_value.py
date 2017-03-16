import math


class GenomeValue(object):
    def __init__(self, lst):
        self._lst = lst
        for j, a in enumerate(self._lst):
            if a < 0:
                self._lst[j] = a - math.floor(a)
            else:
                self._lst[j] = math.fabs(a - math.ceil(a))
        self._index = 0

    def get(self, min_max_dict, is_int=True):
        val = self._lst[self._index] * (min_max_dict['max'] - min_max_dict['min']) + min_max_dict['min']
        self._index += 1
        if is_int:
            return int(round(val))
        return val
