class LoadedTrainedRegressor(object):
    def __init__(self, loader):
        self._trained_regressor = loader.load()

    def predict_proba(self, *args, **kwargs):
        return self._trained_regressor(*args, **kwargs)
