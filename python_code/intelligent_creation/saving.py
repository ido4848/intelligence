import pickle


class Saver(object):
    @staticmethod
    def save(self, py_object, save_path):
        with open(save_path, 'wb') as writeable:
            pickle.dump(py_object, writeable)

    @staticmethod
    def load(save_path):
        with open(save_path, 'rb') as readable:
            return pickle.load(readable)
