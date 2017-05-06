from intelligence.utilization.general_utilities.loggers.console_logger import ConsoleLogger


class ObtentionSetupExecuter(object):
    def __init__(self, obtainer, saver, logger=ConsoleLogger(verbose=True)):
        self._obtainer = obtainer
        self._saver = saver

        self._logger = logger

    def execute(self):
        obtained_items = self._obtainer.obtain()
        self._saver.save(obtained_items)
