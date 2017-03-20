from utilization.general_utilities.loggers.logger import Logger, LOG_LEVELS


class ObtentionSetupExecuter(object):
    def __init__(self, obtainer, saver, verbose=True):
        self._obtainer = obtainer
        self._saver = saver

        self._logger = Logger(who=self.__class__.__name__, verbose=verbose)

    def execute(self):
        obtained_items = self._obtainer.obtain()
        self._saver.save(obtained_items)
