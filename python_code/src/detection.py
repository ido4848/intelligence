import numpy as np

from outer_modules.lsanomaly import LSAnomaly
from util_modules import logging as logger


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
                    logger.log("Could not extract features from item: {}".format(e.message))

        try:
            self._clf.fit(np.array(train_data))
        except Exception as e:
            raise e

        if self._verbose:
            logger.log("Detector was trained using {} items".format(len(train_data)))

    def detect(self, item):
        test_data = self._item_to_features(item)

        try:
            pred = self._clf.predict_proba(np.array([test_data]))
            return pred[0][0]
        except Exception as e:
            if self._verbose:
                logger.log("Could not predict_proba, moving to regular predict, with error: ".format(e.message))

        try:
            pred = self._clf.predict(np.array([test_data]))
            return pred[0]
        except Exception as e:
            raise e
