from intelligence.utilization.general_utilities.loggers.logger import Logger


class CreationExecuter(object):
    def __init__(self, creator, product_saver, num_of_products, verbose=True):
        self._creator = creator
        self._product_saver = product_saver
        self._num_of_products = num_of_products

        self._logger = Logger(who=self.__class__.__name__, verbose=verbose)

    def execute(self):
        products = self._creator.create_many(self._num_of_products)
        for product in products:
            self._product_saver.save(product)
