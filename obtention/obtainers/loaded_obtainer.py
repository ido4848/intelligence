class LoadedObtainer(object):
    def __init__(self, loader):
        self._obtainer = loader.load()

    def obtain(self, *args, **kwargs):
        return self._obtainer.obtain(*args, **kwargs)
