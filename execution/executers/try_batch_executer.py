import traceback
from utilization.general_utilities import logging as logger


class TryBatchExecuter(object):
    def __init__(self, executers):
        self._executers = executers

    def execute(self):
        index = len(self._executers) - 1
        caught = True
        while caught:
            caught = False
            for i in range(index, len(self._executers)):
                current_executer = self._executers[i]
                try:
                    current_executer.execute()
                except Exception as e:
                    if i > index or index == 0:
                        logger.log(
                            "Stopping execution on index {} of {}, because of error {}".format(i + 1,
                                                                                               len(self._executers),
                                                                                               traceback.format_exc()),
                            who=self.__class__.__name__)

                    else:
                        logger.log(
                            "Stopping execution on index {} of {}, because of error {}".format(i + 1,
                                                                                               len(self._executers),
                                                                                               traceback.format_exc()),
                            who=self.__class__.__name__)
                        logger.log("Going to start execution on index {} of {}".format(i, len(self._executers)),
                                   who=self.__class__.__name__)
                        caught = True
                        index -= 1
                        break

        for executer in self._executers:
            executer.execute()
