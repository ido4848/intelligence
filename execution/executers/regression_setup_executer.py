from utilization.general_utilities import logging as logger

'''

1 - part of the data
0 - not part of the data

'''


class RegressionSetupExecuter(object):
    def __init__(self, regressor, train_args_obtainer, item_to_feature_list, saver, verbose=True):
        self._regressor = regressor
        self._train_args_obtainer = train_args_obtainer
        self._saver = saver
        self._item_to_feature_list = item_to_feature_list

        self._verbose = verbose

    def _train(self):
        if self._verbose:
            logger.log("Training started", who=self.__class__.__name__)
        train_args = self._train_args_obtainer.obtain()
        self._regressor.fit(*train_args)
        if self._verbose:
            logger.log("Training finished", who=self.__class__.__name__)

    def execute(self):
        self._train()

        data = {'regressor': self._regressor, 'item_to_feature_list': self._item_to_feature_list}

        self._saver.save(data)
