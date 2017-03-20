from utilization.general_utilities.loggers.logger import Logger, LOG_LEVELS

'''

1 - part of the data
0 - not part of the data

'''


'''
TODO: should not get both item_to_feature_list and train_args_obtainer
something like item_to_feature_list and data_obtainer (generic data obtainer...)
'''

class RegressionSetupExecuter(object):
    def __init__(self, regressor, train_args_obtainer, item_to_feature_list, saver, verbose=True):
        self._regressor = regressor
        self._train_args_obtainer = train_args_obtainer
        self._saver = saver
        self._item_to_feature_list = item_to_feature_list

        self._logger = Logger(who=self.__class__.__name__, verbose=verbose)

    def _train(self):
        self._logger.log("Train was started")
        train_args = self._train_args_obtainer.obtain()
        self._regressor.fit(*train_args)
        self._logger.log("Train was finished")

    def execute(self):
        self._train()

        data = {'regressor': self._regressor, 'item_to_feature_list': self._item_to_feature_list}

        self._saver.save(data)
