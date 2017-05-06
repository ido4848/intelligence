import cPickle
import os
import shelve

from intelligence.utilization.general_utilities.loggers.console_logger import ConsoleLogger
from intelligence.utilization.general_utilities.caring import str_preview


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
                 logger=ConsoleLogger(verbose=True)):
        self._folder_path = folder_path
        self._file_path = file_path
        self._save_method = save_method
        self._file_extension = file_extension
        self._full_path = os.path.join(self._folder_path, self._file_path + self._file_extension)

        self._logger = logger

    def save(self, py_object):
        self._logger.log("Save to {} was started.".format(str_preview(self._full_path)))
        create_folder_if_needed(self._folder_path)
        self._save_method(self._full_path, py_object)
        self._logger.log("Save {} to {} was finished.".format(str_preview(py_object), str_preview(self._full_path)))
