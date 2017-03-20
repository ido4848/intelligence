from utilization.general_utilities.loggers.logger import Logger, LOG_LEVELS


def unit_method(data):
    return data


class EditObtainer(object):
    def __init__(self, obtainer, edit_method=unit_method, verbose=True):
        self._obtainer = obtainer
        self._edit_method = edit_method

        self._verbose = verbose
        self._logger = Logger(who=self.__class__.__name__, verbose=verbose)

    def obtain(self):
        data = self._obtainer.obtain()
        return self._edit_method(data, verbose=self._verbose)
