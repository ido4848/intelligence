from file_saver import FileSaver, shelve_save, pickle_save


class BatchFileSaver(object):
    def __init__(self, folder_path, file_path, file_saver_class=FileSaver, file_extension="", save_method=shelve_save,
                 verbose=False):
        self._folder_path = folder_path
        self._file_path = file_path
        self._save_method = save_method
        self._file_extension = file_extension
        self._verbose = verbose

        self._file_saver_class = file_saver_class
        self._index = 1

    def save(self, py_object):
        fs = self._file_saver_class(self._folder_path, self._file_path + "_" + str(self._index), self._file_extension,
                                    self._save_method, verbose=self._verbose)
        fs.save(py_object)
        self._index += 1
