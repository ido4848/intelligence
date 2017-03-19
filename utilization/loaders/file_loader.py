import os

import shelve
import cPickle

from utilization.general_utilities import logging as logger


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
        self._verbose = verbose

    def load(self):
        if not os.path.isfile(self._save_path):
            raise Exception("cannot load from path {}, id does not exist".format(self._save_path))

        item = self._load_method(self._save_path)
        if self._verbose:
            logger.log("{} was loaded from {}".format(item, self._save_path), who=self.__class__.__name__)
        return item
