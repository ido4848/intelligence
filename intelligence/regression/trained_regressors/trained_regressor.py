import numpy as np

from intelligence.utilization.general_utilities.loggers.logger import Logger


class TrainedRegresor(object):
    def __init__(self, regressor, item_to_feature_list, verbose=True):
        self._regressor = regressor
        self._item_to_feature_list = item_to_feature_list
        self._logger = Logger(who=self.__class__.__name__, verbose=verbose)

    def predict_proba(self, item):
        feature_list = self._item_to_feature_list(item)
        prediction = self._regressor.predict_proba(np.array([feature_list]))[0]
        try:
            return prediction[0]
        except:
            return prediction
