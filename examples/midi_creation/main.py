import os
import sys

from lsanomaly import LSAnomaly

from intelligence.utilization.loaders.file_loader import FileLoader
from intelligence.utilization.savers.batch_file_saver import BatchFileSaver
from intelligence.utilization.savers.timestamp_file_saver import TimestampFileSaver
from intelligence.utilization.savers.file_saver import FileSaver
from intelligence.utilization.general_utilities.loggers.file_logger import FileLogger
from intelligence.utilization.general_utilities.loggers.console_logger import ConsoleLogger

from intelligence.obtention.obtainers.edit_obtainer import EditObtainer
from intelligence.obtention.obtainers.folder_crawler_obtainer import FolderCrawlerObtainer
from intelligence.obtention.obtainers.loaded_data_obtainer import LoadedDataObtainer

from intelligence.regression.trained_regressors.loaded_trained_regressor import LoadedTrainedRegressor

from intelligence.creation.creators.deap_creator import DeapCreator

from intelligence.execution.executers.batch_executer import BatchExecuter
from intelligence.execution.executers.creation_executer import CreationExecuter
from intelligence.execution.executers.obtention_setup_executer import ObtentionSetupExecuter
from intelligence.execution.executers.regression_setup_executer import RegressionSetupExecuter
from intelligence.execution.executers.try_batch_executer import TryBatchExecuter

from midi_helper import VALUE_LIST_SIZE, load_midi, save_midi, midi_to_feature_list, midis_to_train_data, \
    value_list_to_midi


def main(log_file_path=""):
    # CONFIG

    home_folder = "/home/ido"
    music_folder = "Music"
    db_folder = "DB"
    data_folder = "intelligent_data"
    regressor_folder = "intelligent_regressor"
    product_folder = "intelligent_music"
    train_folder = "train"

    name = "test"
    train_name = "midi_{}_train".format(name)
    data_name = "midi_{}_data".format(name)
    regressor_name = "midi_{}_regressor".format(name)
    product_name = "midi_{}_created".format(name)

    execution_configs = [
        {
            'creation_config':
                {'num_of_generations': 1, 'population_size': 10, 'genome_size': VALUE_LIST_SIZE},
            'num_of_products': 10
        },
        {
            'creation_config':
                {'num_of_generations': 1, 'population_size': 15, 'genome_size': VALUE_LIST_SIZE},
            'num_of_products': 15
        }
    ]

    # LOGGERS

    global_logger = ConsoleLogger(verbose=True)
    if log_file_path != "":
        global_logger = FileLogger(log_file_path, verbose=True)

    # SAVERS and LOADERS

    train_data_saver = FileSaver(os.path.join(home_folder, db_folder, data_folder, data_name), data_name, logger=global_logger)
    train_data_loader = FileLoader(os.path.join(home_folder, db_folder, data_folder, data_name, data_name),
                                   logger=global_logger)

    regressor_saver = FileSaver(os.path.join(home_folder, db_folder, regressor_folder, regressor_name), regressor_name,
                                logger=global_logger)
    regressor_loader = FileLoader(
        os.path.join(home_folder, db_folder, regressor_folder, regressor_name, regressor_name), logger=global_logger)

    midi_file_saver = BatchFileSaver(os.path.join(home_folder, music_folder, product_folder, product_name),
                                     product_name, logger=global_logger,
                                     file_saver_class=TimestampFileSaver, file_extension=".mid", save_method=save_midi)
    # OBTAINERS

    midi_train_files_obtainer = FolderCrawlerObtainer(load_midi, os.path.join(home_folder, music_folder, train_folder,
                                                                              train_name), logger=global_logger)
    train_data_obtainer = LoadedDataObtainer(train_data_loader)

    train_args_obtainer = EditObtainer(train_data_obtainer, logger=global_logger, edit_method=midis_to_train_data)

    # TRAINED REGRESSORS

    regressor = LSAnomaly()
    ltr = LoadedTrainedRegressor(regressor_loader)

    # CREATORS

    creators = []
    for j, execution_config in enumerate(execution_configs):
        execution_config['creator'] = DeapCreator(ltr, value_list_to_midi, execution_config['creation_config'],
                                                  logger=global_logger)
        execution_configs[j] = execution_config

    # EXECUTERS

    ose = ObtentionSetupExecuter(midi_train_files_obtainer, train_data_saver, logger=global_logger)
    rse = RegressionSetupExecuter(regressor, train_args_obtainer, midi_to_feature_list, regressor_saver, logger=global_logger)

    creation_executers = [
        CreationExecuter(execution_config['creator'], midi_file_saver, execution_config['num_of_products'],
                         logger=global_logger)
        for execution_config in execution_configs]

    try_batch_executers = [TryBatchExecuter([ose, rse, ce], logger=global_logger) for ce in creation_executers]

    be = BatchExecuter(try_batch_executers)

    be.execute()


if __name__ == "__main__":
    log_file_path = ""
    if len(sys.argv) > 1:
        log_file_path = sys.argv[1]
    main(log_file_path)

'''
all should get as last param logger

TODO:

GANS?
LSTM?

split big midis (smart split?)
create small midis
constants? (midi length, instruments number, what instruments)
info file for each created
more generic saver?
crawl the web?
generic_multiple_main? (shortcut)
normalize featuers ( x - avg/(max-min))

better loggers!!!!1
tfrecords?
'''
