class LoadedDataObtainer(object):
    def __init__(self, loader):
        self._loader = loader
        self._data = None

    def obtain(self):
        if self._data is None:
            self._data = self._loader.load()
        return self._data
