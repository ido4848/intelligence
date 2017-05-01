from intelligence.utilization.general_utilities.loggers.logger import Logger
from intelligence.utilization.value_lists.random_value_list import RandomValueList


class RandomCreator(object):
    def __init__(self, value_list_to_item, verbose=True):
        self._value_list_to_item = value_list_to_item

        self._logger = Logger(who=self.__class__.__name__, verbose=verbose)

    def create(self):
        value_list = RandomValueList()
        return self._value_list_to_item(value_list)

    def create_many(self, n):
        return [self.create() for _ in range(n)]
