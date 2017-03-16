import math


class GenomeValue(object):
    def __init__(self, lst):
        self.lst = lst
        for j, a in enumerate(self.lst):
            if a < 0:
                self.lst[j] = a - math.floor(a)
            else:
                self.lst[j] = math.fabs(a - math.ceil(a))
        self.index = 0

    def get(self, min_max_dict, is_int=True):
        val = self.lst[self.index] * (min_max_dict['max'] - min_max_dict['min']) + min_max_dict['min']
        self.index += 1
        if is_int:
            return int(round(val))
        return val
