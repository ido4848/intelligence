import numpy as np

from utilization.general_utilities.caring import apply_carefully

'''

1 - part of the data
0 - not part of the data

'''


class OneClassTrainedRegresor(object):
    def __init__(self, regressor, positive_items_obtainer, item_to_feature_list, verbose=True):
        self._regressor = regressor
        self._positive_items_obtainer = positive_items_obtainer
        self._item_to_feature_list = item_to_feature_list

        self._verbose = verbose

        self._train()

    def _train(self):
        positive_items = self._positive_items_obtainer.obtain()
        positive_feature_lists = apply_carefully(positive_items, self._item_to_feature_list, self._verbose)
        self._regressor.fit(np.array(positive_feature_lists))

    def predict_proba(self, item):
        feature_list = self._item_to_feature_list(item)
        prediction = self._regressor.predict_proba(np.array(feature_list))
        if isinstance(prediction, list):
            return prediction[0]
        else:
            return prediction
