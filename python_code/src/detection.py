import shelve

import numpy as np
from lsanomaly import LSAnomaly

from util_modules import logging as logger


class Detector(object):
    def __init__(self, positive_set, negative_set, item_to_features, clf=None, verbose=True, train=True):
        self._positive_set = positive_set
        self._negative_set = negative_set
        self._item_to_features = item_to_features

        if clf is not None:
            self._clf = clf
        else:
            if self._negative_set is None:
                self._clf = LSAnomaly()
            else:
                self._clf = None  # TODO: update

        self._verbose = verbose
        if train:
            self._train()

    def _items_to_features_verbose(self, items):
        if not isinstance(items, list):
            if self._verbose:
                logger.log("items {} are not a list".format(items))
        features = []
        for item in items:
            try:
                features.append(self._item_to_features(item))
            except Exception as e:
                if self._verbose:
                    logger.log("Could not extract features from item: {}".format(e.message))
        return features

    # TODO: update for negative set too
    def _train(self):
        positive_train_data = self._items_to_features_verbose(self._positive_set)
        negative_train_data = self._items_to_features_verbose(self._negative_set)

        try:
            if len(negative_train_data) > 0:
                self._clf.fit(np.array(positive_train_data), np.array(negative_train_data))
            else:
                self._clf.fit(np.array(positive_train_data))
        except Exception as e:
            raise e

        if self._verbose:
            logger.log("Detector was trained using {} items".format(len(positive_train_data)))

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

    def saveToFile(self, save_path):
        db = shelve.open(save_path)
        db['_clf'] = self._clf
        db.close()


def loadFromFile(save_path, item_to_features):
    db = shelve.open(save_path)
    detector_obj = Detector(None, None, None, train=False)
    detector_obj._item_to_features = item_to_features
    detector_obj._clf = db['_clf']
    db.close()
    return detector_obj
