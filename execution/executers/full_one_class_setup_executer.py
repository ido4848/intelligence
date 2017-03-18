from obtention_setup_executer import ObtentionSetupExecuter
from one_class_regression_setup_executer import OneClassRegressionSetupExecuter
from batch_executer import BatchExecuter

class FullOneClassSetupExecuter(object):
    def __init__(self, obtainer, obtainer_saver, regressor, positive_items_obtainer, item_to_feature_list,
                 regressor_saver, verbose=True):
    self._executers =
