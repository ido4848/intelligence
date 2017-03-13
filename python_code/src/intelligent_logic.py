import time
import datetime
import os

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


def create_folder_if_needed(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def generic_main(executions_args):
    for arg in executions_args:
        product_name = arg['data_name'] + "_created_" + arg['index']
        data_name = arg['data_name'] + "_data"
        detector_name = arg['data_name'] + "_detector"

        time_path = datetime.datetime.now().strftime("/%y_%m_%d/%H_%M_%S")
        train_folder_path = arg['home_folder'] + arg['type_folder'] + "/train/" + arg['train_name']

        db_folder_path = arg['home_folder'] + "/DB/intelligent_data/" + data_name
        detector_folder_path = arg['home_folder'] + "/DB/intelligent_detectors/" + detector_name
        product_folder_path = arg['home_folder'] + arg['type_folder'] + time_path + "/" + product_name

        db_file_path = db_folder_path + "/" + detector_name
        detector_file_path = detector_folder_path + "/" + data_name
        product_file_path = product_folder_path + "/" + product_name + "." + arg['file_extension']

        create_folder_if_needed(db_folder_path)
        create_folder_if_needed(detector_folder_path)
        create_folder_if_needed(product_folder_path)

        main_logic(arg['functions'], train_folder_path, arg['iterations'], arg['freq_stats'], product_file_path,
                   data_path=db_file_path,
                   detector_path=detector_file_path, setup=arg['setup'], verbose=arg['verbose'])


def generic_type_main(execution_args, home_folder, type_folder, file_extension, functions):
    for j, arg in enumerate(execution_args):
        arg['home_folder'] = home_folder
        arg['type_folder'] = type_folder
        arg['file_extension'] = file_extension
        arg['functions'] = functions
        arg['index'] = str(j + 1)
    generic_main(execution_args)
