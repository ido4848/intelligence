import traceback
from utilization.general_utilities import logging as logger


# TODO: less code duplication

class TryBatchExecuter(object):
    def __init__(self, executers, verbose=True):
        self._executers = executers
        self._verbose = verbose

    def execute(self):
        index = len(self._executers) - 1
        caught = True
        if self._verbose:
            logger.log("Starting execution on index {} of {}: {}".format(index + 1, len(self._executers),
                                                                         self._executers[index]),
                       who=self.__class__.__name__)
        while caught:
            caught = False
            for i in range(index, len(self._executers)):
                current_executer = self._executers[i]
                try:
                    current_executer.execute()
                except Exception as e:
                    if self._verbose:
                        logger.log(
                            "Stopping execution on index {} of {}: {}, because of error {}".format(i + 1,
                                                                                                   len(
                                                                                                       self._executers),
                                                                                                   current_executer,
                                                                                                   traceback.format_exc()),
                            who=self.__class__.__name__)

                    if i > index or index == 0:
                        return
                    else:
                        if self._verbose:
                            logger.log(
                                "Stopping execution on index {} of {}: {}, because of error {}".format(i + 1,
                                                                                                       len(
                                                                                                           self._executers),
                                                                                                       current_executer,
                                                                                                       traceback.format_exc()),
                                who=self.__class__.__name__)
                            logger.log("Starting execution on index {} of {}: {}".format(i, len(self._executers),
                                                                                         self._executers[i - 1]),
                                       who=self.__class__.__name__)
                        caught = True
                        index -= 1
                        break
