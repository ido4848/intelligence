import os
import shelve
import cPickle

from utilization.general_utilities import logging as logger


def shelve_save(path, py_object):
    db = shelve.open(path)
    db['data'] = py_object
    db.close()


def pickle_save(path, py_object):
    with open(path, 'wb') as f:
        cPickle.dump(py_object, f)


def create_folder_if_needed(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


class FileSaver(object):
    def __init__(self, folder_path, file_path, file_extension="", save_method=shelve_save,
                 verbose=True):
        self._folder_path = folder_path
        self._file_path = file_path
        self._save_method = save_method
        self._file_extension = file_extension
        self._full_path = os.path.join(self._folder_path, self._file_path + self._file_extension)

        self._verbose = verbose

    def save(self, py_object):
        create_folder_if_needed(self._folder_path)
        self._save_method(self._full_path, py_object)
        if self._verbose:
            logger.log("{} was saved to {}".format(py_object, self._full_path), who=self.__class__.__name__)
