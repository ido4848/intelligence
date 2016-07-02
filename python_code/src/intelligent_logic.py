import crawling
import creation
import detection

from util_modules import saving as saver
from util_modules import logging as logger


def main_logic(functions, positive_folder, iterations, freq_stats, item_path,
               detector_path=None, setup=True, verbose=True):
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
        if detector_path is not None:
            saver.save(detector, detector_path)
            if verbose:
                logger.log("Detector was saved.")
    elif detector_path is not None:
        detector = saver.load(detector_path)
        if verbose:
            logger.log("Detector was loaded from file.")
    else:
        logger.log("Could not get detector, as setup is False and there is no saved detector.")
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
        logger.log("Best item was saved.")
