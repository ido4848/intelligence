import shelve


def shelve_load(path):
    db = shelve.open(path)
    value = db['data']
    db.close()
    return value


class FileLoader(object):
    def __init__(self, save_path, load_method=shelve_load):
        self._save_path = save_path
        self._load_method = load_method

    def load(self):
        return self._load_method(self._save_path)
