import traceback

from intelligent_creation.utilization.general_utilities.loggers.logger import Logger


# TODO: less code duplication

class TryBatchExecuter(object):
    def __init__(self, executers, verbose=True):
        self._executers = executers
        self._logger = Logger(who=self.__class__.__name__, verbose=verbose)

    def execute(self):
        index = len(self._executers) - 1
        caught = True
        self._logger.log("Starting execution on index {} of {}: {}".format(index + 1, len(self._executers),
                                                                           self._executers[index]))
        while caught:
            caught = False
            for i in range(index, len(self._executers)):
                current_executer = self._executers[i]
                try:
                    current_executer.execute()
                except Exception as e:
                    self._logger.log(
                        "Stopping execution on index {} of {}: {}, because of error {}".format(i + 1,
                                                                                               len(
                                                                                                   self._executers),
                                                                                               current_executer,
                                                                                               traceback.format_exc()))

                    if i > index or index == 0:
                        return
                    else:
                        self._logger.log(
                            "Stopping execution on index {} of {}: {}, because of error {}".format(i + 1,
                                                                                                   len(
                                                                                                       self._executers),
                                                                                                   current_executer,
                                                                                                   traceback.format_exc()))
                        self._logger.log("Starting execution on index {} of {}: {}".format(i, len(self._executers),
                                                                                           self._executers[i - 1]))
                    caught = True
                    index -= 1
                    break
