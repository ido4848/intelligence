import numpy as np

from utilization.general_utilities import logging as logger


class TrainedRegresor(object):
    def __init__(self, regressor, item_to_feature_list, verbose=True):
        self._regressor = regressor
        self._item_to_feature_list = item_to_feature_list
        self._verbose = verbose

    def predict_proba(self, item):
        feature_list = self._item_to_feature_list(item)
        prediction = self._regressor.predict_proba(np.array(feature_list))
        if isinstance(prediction, list):
            return prediction[0]
        else:
            return prediction
