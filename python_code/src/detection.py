import numpy as np

from outer_modules.lsanomaly import LSAnomaly


class Detector(object):
    def __init__(self, positive_set, negative_set, item_to_features, verbose=True):
        self._positive_set = positive_set
        self._negative_set = negative_set
        self._item_to_features = item_to_features
        if self._negative_set is None:
            self._clf = LSAnomaly()
        else:
            self._clf = None  # TODO: update

        self._verbose = verbose
        self._train()

    # TODO: update for negative set too
    def _train(self):
        train_data = []
        for item in self._positive_set:
            try:
                train_data.append(self._item_to_features(item))
            except Exception as e:
                if self._verbose:
                    print "Could not extract features from item: {}".format(e.message)

        try:
            self._clf.fit(np.array(train_data))
        except Exception as e:
            raise e

    def detect(self, item):
        test_data = self._item_to_features(item)

        try:
            pred = self._clf.predict_proba(np.array([test_data]))
            return pred[0][0]
        except Exception as e:
            if self._verbose:
                print "Could not predict_proba, moving to regular predict"

        try:
            pred = self._clf.predict(np.array([test_data]))
            return pred[0]
        except Exception as e:
            raise e
