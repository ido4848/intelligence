import os

import shelve
import cPickle

from utilization.general_utilities.loggers.logger import Logger, LOG_LEVELS


def shelve_load(path):
    db = shelve.open(path)
    value = db['data']
    db.close()
    return value


def pickle_load(path):
    with open(path, 'rb') as f:
        return cPickle.load(f)


class FileLoader(object):
    def __init__(self, save_path, load_method=shelve_load, verbose=True):
        self._save_path = save_path
        self._load_method = load_method

        self._logger = Logger(who=self.__class__.__name__, verbose=verbose)

    def load(self):
        self._logger.log("Load from {} was started.".format(self._save_path))
        if not os.path.isfile(self._save_path):
            raise Exception("cannot load from path {}, file does not exist".format(self._save_path))

        item = self._load_method(self._save_path)
        self._logger.log("Load {} from {} was finished".format(item, self._save_path))
        return item
