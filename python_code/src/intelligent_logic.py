import time

import crawling
import creation
import detection

from util_modules import saving as saver
from util_modules import logging as logger

def main_logic(functions, positive_folder, iterations, freq_stats, item_path,
               data_path=None, detector_path=None, setup=True, verbose=True):
    start_time = time.time()
    if verbose:
        logger.log("Starting to perform main logic.")
    detector = None
    if setup:
        positive_set = crawling.FolderCrawler.crawl(positive_folder, functions['path_to_item'])
        if verbose:
            logger.log("Crawling ended.")
        detector = detection.Detector(positive_set, None, functions['item_to_features'])
        if verbose:
            logger.log("Detector creation has ended.")
        if data_path is not None:
            saver.save(positive_set, data_path)
            if verbose:
                logger.log("Crawled data was saved.")
        if detector_path is not None:
            detector.saveToFile(detector_path)
            if verbose:
                logger.log("Detector was saved.")
    elif detector_path is not None:
        detector = detection.loadFromFile(detector_path, functions['item_to_features'])
        if verbose:
            logger.log("Detector was loaded from file {}.".format(detector_path))
    elif data_path is not None:
        positive_set = saver.load(data_path)
        if verbose:
            logger.log("Crawled data was loaded from file {}.".format(data_path))
        detector = detection.Detector(positive_set, None, functions['item_to_features'])

    else:
        logger.log("Could not get crawled data, as setup is False and there is no saved data.")
        return

    creator = creation.Creator(detector, functions['get_item_genome'], functions['genome_to_item'])
    if verbose:
        logger.log("Creator creation has ended.")
        logger.log("Best item creation has started.")
    best_item = functions['genome_to_item'](creator.create(iterations, freq_stats))
    if verbose:
        logger.log("Best item creation has ended.")
    functions['save_item'](best_item, item_path)
    if verbose:
        logger.log("Best item was saved in {}.".format(item_path))

    end_time = time.time()
    if verbose:
        logger.log("It took {} seconds".format(end_time - start_time))