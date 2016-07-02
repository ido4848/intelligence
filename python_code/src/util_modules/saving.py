import pickle


def save(py_object, save_path):
    with open(save_path, 'wb') as writeable:
        pickle.dump(py_object, writeable)


def load(save_path):
    with open(save_path, 'rb') as readable:
        return pickle.load(readable)
