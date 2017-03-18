from regression.trained_regressors.two_class_trained_regressor import TwoClassTrainedRegresor


class OneClassRegressionSetupExecuter(object):
    def __init__(self, regressor, positive_items_obtainer, negative_items_obtainer, item_to_feature_list, saver,
                 verbose=True):
        self._regressor = regressor
        self._positive_items_obtainer = positive_items_obtainer
        self._negative_items_obtainer = negative_items_obtainer
        self._item_to_feature_list = item_to_feature_list
        self._saver = saver

        self._verbose = verbose

    def execute(self):
        trained_regressor = TwoClassTrainedRegresor(self._regressor, self._positive_items_obtainer,
                                                    self._negative_items_obtainer,
                                                    self._item_to_feature_list, self._verbose)
        self._saver.save(trained_regressor)
