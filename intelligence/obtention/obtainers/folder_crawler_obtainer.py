import os

from intelligence.utilization.general_utilities.loggers.logger import Logger

'''
TODO:
Could be more generic,
a generic loaderObtainer, that gets loader as input
'''


class FolderCrawlerObtainer(object):
    def __init__(self, path_to_item, folder, verbose=True):
        self._path_to_item = path_to_item
        self._logger = Logger(who=self.__class__.__name__, verbose=verbose)
        self._folder = folder

    def _crawl(self, folder):
        self._logger.log("crawling started on {}".format(folder))
        items = []
        for root, _, file_names in os.walk(folder):
            for file_name in file_names:
                full_path = root + "/" + file_name
                try:
                    items.append(self._path_to_item(full_path))
                except Exception as e:
                    self._logger.log("Could not create item from path {} : {}".format(full_path, e.message))

        self._logger.log("{} items were crawled.".format(len(items)))
        return items

    def obtain(self):
        return self._crawl(self._folder)
