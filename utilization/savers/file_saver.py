import os
import shelve


def shelve_save(path, py_object):
    db = shelve.open(path)
    db['data'] = py_object
    db.close()


def create_folder_if_needed(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


class FileSaver(object):
    def __init__(self, folder_path, file_path, file_extension="", save_method=shelve_save):
        self._folder_path = folder_path
        self._file_path = file_path
        self._save_method = save_method
        self._file_extension = file_extension

    def save(self, py_object):
        create_folder_if_needed(self._folder_path)
        return self._save_method(os.path.join(self._folder_path, self._file_path + self._file_extension), py_object)
