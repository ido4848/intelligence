import random


class RandomValueList(object):
    def __init__(self):
        pass

    def get(self, min_max_dict, is_int=True):
        if is_int:
            return random.randint(min_max_dict['min'], min_max_dict['max'])
        return random.random() * (min_max_dict['max'] - min_max_dict['min']) + min_max_dict['min']
