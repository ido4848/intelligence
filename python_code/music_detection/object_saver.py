import shelve


class ObjectSaver(object):
    def __init__(self):
        pass

    @staticmethod
    def save_to_file(obj, file_path):
        db = shelve.open(file_path)
        db["object"] = obj
        db.close()

    @staticmethod
    def load_from_file(file_path):
        db = shelve.open(file_path)
        obj = db["object"]
        db.close()
        return db
