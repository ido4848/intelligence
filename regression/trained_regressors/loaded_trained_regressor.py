from trained_regressor import TrainedRegresor


class LoadedTrainedRegressor(object):
    def __init__(self, loader):
        self._loader = loader
        self._regressor = None
        self._trained_regressor = None
        self._item_to_feature_list = None

    def predict_proba(self, *args, **kwargs):
        if self._trained_regressor is None:
            data = self._loader.load()
            self._regressor = data['regressor']
            self._item_to_feature_list = data['item_to_feature_list']

            self._trained_regressor = TrainedRegresor(self._regressor, self._item_to_feature_list)
        return self._trained_regressor.predict_proba(*args, **kwargs)
