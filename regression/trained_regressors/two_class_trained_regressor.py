import numpy as np

from utilization.general_utilities.caring import apply_carefully

'''

1 - part of the data
0 - not part of the data

'''


class TwoClassTrainedRegresor(object):
    def __init__(self, regressor, positive_items_obtainer, negative_items_obtainer, item_to_feature_list, verbose=True):
        self._regressor = regressor
        self._positive_items_obtainer = positive_items_obtainer
        self._negative_items_obtainer = negative_items_obtainer
        self._item_to_feature_list = item_to_feature_list

        self._verbose = verbose

        self._train()

    def _train(self):
        positive_items = self._positive_items_obtainer.obtain()
        negative_items = self._negative_items_obtainer.obtain()

        positive_feature_lists = apply_carefully(positive_items, self._item_to_feature_list, self._verbose)
        negative_feature_lists = apply_carefully(negative_items, self._item_to_feature_list, self._verbose)

        items = positive_feature_lists + negative_feature_lists
        labels = [1 for _ in positive_feature_lists] + [0 for _ in negative_feature_lists]

        self._regressor.fit(np.array(items), np.array(labels))

    def predict_proba(self, item):
        feature_list = self._item_to_feature_list(item)
        prediction = self._regressor.predict_proba(np.array(feature_list))
        if isinstance(prediction, list):
            return prediction[0]
        else:
            return prediction
