import inspect
import os

import numpy as np

from music21 import features
from music21 import instrument
from music21.chord import Chord
from music21.duration import Duration
from music21.midi import translate
from music21.note import Rest
from music21.stream import Part, Stream
from music21.volume import Volume

from lsanomaly import LSAnomaly

from utilization.savers.file_saver import FileSaver
from utilization.loaders.file_loader import FileLoader
from utilization.savers.timestamp_file_saver import TimestampFileSaver
from utilization.savers.batch_file_saver import BatchFileSaver
from utilization.general_utilities.caring import apply_carefully

from obtention.obtainers.folder_crawler_obtainer import FolderCrawlerObtainer
from obtention.obtainers.loaded_data_obtainer import LoadedDataObtainer
from obtention.obtainers.edit_obtainer import EditObtainer

from regression.trained_regressors.loaded_trained_regressor import LoadedTrainedRegressor

from creation.creators.deap_creator import DeapCreator

from execution.executers.obtention_setup_executer import ObtentionSetupExecuter
from execution.executers.regression_setup_executer import RegressionSetupExecuter
from execution.executers.creation_executer import CreationExecuter
from execution.executers.batch_executer import BatchExecuter
from execution.executers.try_batch_executer import TryBatchExecuter


def flatten(l): return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [
    l]


INSTRUMENTS_CLASSES = []
for _, instrument_class in instrument.__dict__.iteritems():
    if inspect.isclass(instrument_class):
        if issubclass(instrument_class, instrument.Instrument):
            INSTRUMENTS_CLASSES.append(instrument_class)

PITCH = {'min': 36, 'max': 61}
NUM_OF_NOTES = {'min': 1, 'max': 6}
DURATION = {'min': 0.125, 'max': 4.0}
VELOCITY = {'min': 70, 'max': 100}

NUM_OF_PARTS = {'min': 1, 'max': 20}
LENGTH = {'min': 10, 'max': 20}

# note/rest + duration + velocity + num of notes + notes
NOTE_SIZE = 1 + 1 + 1 + 1 + NUM_OF_NOTES['max']

# instrument + note
PART_SIZE = 1 + LENGTH['max'] * NOTE_SIZE

# length + num of parts + parts
VALUE_LIST_SIZE = 1 + 1 + NUM_OF_PARTS['max'] * PART_SIZE


def set_instrument(part, instrument):
    part.insert(0, instrument)


def append_chord(part, notes, duration, velocity):
    c = Chord(notes, duration=Duration(duration))
    c.volume = Volume(velocity=velocity)
    part.append(c)


def append_rest(part, duration):
    part.append(Rest(quarterLength=duration))


def get_part(length, list_value):
    part = Part()
    instrument_index = list_value.get({'min': 0, 'max': len(INSTRUMENTS_CLASSES) - 1})
    instrument_class = INSTRUMENTS_CLASSES[instrument_index]
    set_instrument(part, instrument_class())
    for _ in range(length):
        note_pred = list_value.get({'min': 0, 'max': 1}, is_int=False)
        duration = list_value.get(DURATION, is_int=False)
        is_chord = note_pred > 0.2
        if is_chord:
            num_of_notes = list_value.get(NUM_OF_NOTES)
            velocity = list_value.get(VELOCITY)
            notes = []
            for _ in range(num_of_notes):
                note = list_value.get(PITCH)
                notes.append(note)
            append_chord(part, notes, duration, velocity)
        else:
            append_rest(part, duration)
    return part


def save_midi(save_path, item):
    midi_file = translate.streamToMidiFile(item)
    binfile = open(save_path, 'wb')
    binfile.write(midi_file.writestr())
    binfile.close()


def load_midi(path):
    return translate.midiFilePathToStream(path)


def midi_to_features(stream):
    f = features.base.allFeaturesAsList(stream)
    return flatten(f[0] + f[1])


def value_list_to_midi(value_list):
    length = value_list.get(LENGTH)
    num_of_parts = value_list.get(NUM_OF_PARTS)
    parts = []
    for _ in range(num_of_parts):
        parts.append(get_part(length, value_list))

    stream = Stream(parts)
    return stream


def midis_to_train_data(midis, verbose=True):
    feature_lists = apply_carefully(midis, midi_to_features, verbose)
    train_list = np.array(feature_lists)
    return train_list,


def main():
    # CONFIG

    home_folder = "/home/ido"
    music_folder = "Music"
    db_folder = "DB"
    data_folder = "intelligent_data"
    regressor_folder = "intelligent_regressor"
    product_folder = "intelligent_music"
    train_folder = "train"

    train_name = "midi_test_train"
    data_name = "midi_test_data"
    regressor_name = "midi_test_regressor"
    product_name = "midi_test_created"

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

    # SAVERS and LOADERS

    train_data_saver = FileSaver(os.path.join(home_folder, db_folder, data_folder, data_name), data_name)
    train_data_loader = FileLoader(os.path.join(home_folder, db_folder, data_folder, data_name, data_name))

    regressor_saver = FileSaver(os.path.join(home_folder, db_folder, regressor_folder, regressor_name), regressor_name)
    regressor_loader = FileLoader(
        os.path.join(home_folder, db_folder, regressor_folder, regressor_name, regressor_name))

    midi_file_saver = BatchFileSaver(os.path.join(home_folder, music_folder, product_name), product_name,
                                     file_saver_class=TimestampFileSaver, file_extension=".mid", save_method=save_midi)
    # OBTAINERS

    midi_train_files_obtainer = FolderCrawlerObtainer(load_midi, os.path.join(home_folder, music_folder, train_folder,
                                                                              train_name))
    train_data_obtainer = LoadedDataObtainer(train_data_loader)

    train_args_obtainer = EditObtainer(train_data_obtainer, edit_method=midis_to_train_data)

    # TRAINED REGRESSORS

    regressor = LSAnomaly()
    ltr = LoadedTrainedRegressor(regressor)

    # CREATORS

    creators = []
    for j, execution_config in enumerate(execution_configs):
        execution_config['creator'] = DeapCreator(ltr, value_list_to_midi, execution_config['creation_config'])
        execution_configs[j] = execution_config

    # EXECUTERS

    ose = ObtentionSetupExecuter(midi_train_files_obtainer, train_data_saver)
    rse = RegressionSetupExecuter(regressor, train_args_obtainer, midi_to_features, regressor_saver)

    creation_executers = [
        CreationExecuter(execution_config['creator'], midi_file_saver, execution_config['num_of_products'])
        for execution_config in execution_configs]

    try_batch_executers = [TryBatchExecuter([ose, rse, ce]) for ce in creation_executers]

    be = BatchExecuter(try_batch_executers)

    be.execute()


if __name__ == "__main__":
    main()

'''
TODO:
split big midis (smart split?)
create small midis
constants? (midi length, instruments number, what instruments)
info file for each created
more generic saver?
crawl the web?
generic_multiple_main? (shortcut)
normalize featuers ( x - avg/(max-min))

SHOULD BE UNDER EXAMPLES

SETUPExecuter (that checks if setup is needed)
rename main executer
'''
