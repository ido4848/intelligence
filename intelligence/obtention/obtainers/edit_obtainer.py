from intelligence.utilization.general_utilities.loggers.console_logger import ConsoleLogger


def unit_method(data, logger=ConsoleLogger(verbose=True)):
    return data


class EditObtainer(object):
    def __init__(self, obtainer, edit_method=unit_method, logger=ConsoleLogger(verbose=True)):
        self._obtainer = obtainer
        self._edit_method = edit_method

        self._logger = logger

    def obtain(self):
        data = self._obtainer.obtain()
        return self._edit_method(data, logger=self._logger)
