import os
import datetime

from intelligence.utilization.general_utilities.loggers.console_logger import ConsoleLogger
from file_saver import FileSaver, shelve_save, pickle_save


class TimestampFileSaver(object):
    def __init__(self, folder_path, file_path, file_extension="", save_method=shelve_save,
                 logger=ConsoleLogger(verbose=True)):
        self._folder_path = folder_path
        self._file_path = file_path
        self._save_method = save_method
        self._file_extension = file_extension
        self._logger = logger

    def save(self, py_object):
        time_path = datetime.datetime.now().strftime("%y_%m_%d/%H_%M_%S")
        fs = FileSaver(os.path.join(self._folder_path, time_path), self._file_path, self._file_extension,
                       self._save_method, logger=self._logger)
        return fs.save(py_object)
