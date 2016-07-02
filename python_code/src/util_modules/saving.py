import pickle
import shelve


def save(py_object, save_path):
    db = shelve.open(save_path)
    db['data'] = py_object
    db.close()


def load(save_path):
    db = shelve.open(save_path)
    value = db['data']
    db.close()
    return value


def pickle_save(py_object, save_path):
    with open(save_path, 'wb') as writeable:
        pickle.dump(py_object, writeable)


def pickle_load(save_path):
    with open(save_path, 'rb') as readable:
        return pickle.load(readable)
