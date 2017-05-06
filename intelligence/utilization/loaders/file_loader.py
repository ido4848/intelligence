import cPickle
import os
import shelve

from intelligence.utilization.general_utilities.loggers.console_logger import ConsoleLogger
from intelligence.utilization.general_utilities.caring import str_preview

def shelve_load(path):
    db = shelve.open(path)
    value = db['data']
    db.close()
    return value


def pickle_load(path):
    with open(path, 'rb') as f:
        return cPickle.load(f)


class FileLoader(object):
    def __init__(self, save_path, load_method=shelve_load, logger=ConsoleLogger(verbose=True)):
        self._save_path = save_path
        self._load_method = load_method

        self._logger = logger

    def load(self):
        self._logger.log("Load from {} was started.".format(str_preview(self._save_path)))
        if not os.path.isfile(self._save_path):
            raise Exception("cannot load from path {}, file does not exist".format(self._save_path))

        item = self._load_method(self._save_path)
        self._logger.log("Load {} from {} was finished".format(str_preview(str(item)), str_preview(self._save_path)))
        return item
