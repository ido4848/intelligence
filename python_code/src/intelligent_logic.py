import time
import datetime
import os

import crawling
import creation
import detection

from util_modules import saving as saver
from util_modules import logging as logger

'''
functions:
     path_to_item
     item_to_features
     genome_to_item
     save_item

params:
    population_size
    iterations
    classifier

paths:
    positive_folder
    population_path
    data_path
    detector_path
    product_folder_path

flags:
    one_class_classifier
    setup
    verbose

names:
    product_name

type_params:
    file_extension

'''


def main_logic(functions, params, paths, flags, names, type_params):
    setup = flags.get('setup', False)
    verbose = flags.get('verbose', False)

    start_time = time.time()
    if verbose:
        logger.log("Starting to perform main logic.")
    detector = None
    if setup:
        positive_set = crawling.FolderCrawler.crawl(paths['positive_folder'], functions['path_to_item'])
        negative_set = None
        if verbose:
            logger.log("Crawling ended.")
        if not flags.get("one_class_classifier"):
            negative_set = []  # TODO update
        detector = detection.Detector(positive_set, negative_set, functions['item_to_features'],
                                      clf=params.get('classifier'))
        if verbose:
            logger.log("Detector creation has ended.")
        if 'data_path' in paths.keys():
            saver.save(positive_set, paths['data_path'])
            if verbose:
                logger.log("Crawled data was saved.")
        if 'detector_path' in paths.keys():
            detector.saveToFile(paths['detector_path'])
            if verbose:
                logger.log("Detector was saved.")
    elif 'detector_path' in paths.keys():
        detector = detection.loadFromFile(paths['detector_path'], functions['item_to_features'])
        if verbose:
            logger.log("Detector was loaded from file {}.".format(paths['detector_path']))
    elif 'data_path' in paths.keys():
        positive_set = saver.load(paths['data_path'])
        if verbose:
            logger.log("Crawled data was loaded from file {}.".format(paths['data_path']))
        detector = detection.Detector(positive_set, None, functions['item_to_features'])

    else:
        logger.log("Could not get crawled data, as setup is False and there is no saved data.")
        return

    creator = creation.Creator(detector, functions['genome_to_item'], verbose=verbose)
    if verbose:
        logger.log("Creator creation has ended.")
        logger.log("Best population creation has started.")
    best_population = (creator.create(params))
    best_items = [functions['genome_to_item'](genome) for genome in best_population]
    if verbose:
        logger.log("Best population creation has ended.")
    for j, best_item in enumerate(best_items):
        item_path = "{}/{}_{}.{}".format(paths['product_folder_path'], names['product_name'], str(j + 1),
                                         type_params['file_extension'])
        functions['save_item'](best_item, item_path)
    if verbose:
        logger.log("Best population was saved under {}.".format(paths['product_folder_path']))

    end_time = time.time()
    if verbose:
        logger.log("It took {} seconds".format(end_time - start_time))


def create_folder_if_needed(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


'''
execution_arg:
    home_folder
    params
    functions
    flags
    names:
        product_name
        data_name
        detector_name
        train_name
    type_params:
        type_name
        type_folder
        file_extension
'''


def generic_main(executions_args):
    for arg in executions_args:
        product_name = arg['names']['product_name'] + "_created"
        data_name = arg['names']['data_name'] + "_data"
        detector_name = arg['names']['detector_name'] + "_detector"
        train_name = arg['names']['train_name'] + "_train"

        time_path = datetime.datetime.now().strftime("/%y_%m_%d/%H_%M_%S")
        train_folder_path = arg['home_folder'] + arg['type_params']['type_folder'] + "/train/" + train_name

        db_folder_path = arg['home_folder'] + "/DB/intelligent_data/" + data_name
        detector_folder_path = arg['home_folder'] + "/DB/intelligent_detectors/" + detector_name
        product_folder_path = arg['home_folder'] + arg['type_params']['type_folder'] + "/intelligent_" + \
                              arg['type_params'][
                                  'type_name'] + time_path + "/" + product_name

        db_file_path = db_folder_path + "/" + detector_name
        detector_file_path = detector_folder_path + "/" + data_name

        create_folder_if_needed(db_folder_path)
        create_folder_if_needed(detector_folder_path)
        create_folder_if_needed(product_folder_path)

        paths = {
            'positive_folder': train_folder_path,
            'product_path': product_folder_path,
            'data_path': db_file_path,
            'detector_path': detector_file_path,
            'product_folder_path': product_folder_path
        }

        main_logic(arg['functions'], arg['params'], paths, arg['flags'], arg['names'], arg['type_params'])
