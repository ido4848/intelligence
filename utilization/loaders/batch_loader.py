class BatchLoader(object):
    def __init__(self, loaders, verbose=True):
        self._loaders = loaders
        self._verbose = verbose

    def load(self):

        if not os.path.isfile(self._save_path):
            raise Exception("cannot load from path {}, id does not exist".format(self._save_path))

        item = self._load_method(self._save_path)
        if self._verbose:
            logger.log("{} was loaded from {}".format(item, self._save_path), who=self.__class__.__name__)
        return item
