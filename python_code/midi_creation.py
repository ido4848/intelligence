import inspect

from music21 import features
from music21.midi import translate
from music21.stream import Part, Stream
from music21.chord import Chord
from music21.note import Note, Rest
from music21.duration import Duration
from music21 import instrument
from music21.volume import Volume

import src.intelligent_logic


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
GENOME_SIZE = 1 + 1 + NUM_OF_PARTS['max'] * PART_SIZE


def set_instrument(part, instrument):
    part.insert(0, instrument)


def append_chord(part, notes, duration, velocity):
    c = Chord(notes, duration=Duration(duration))
    c.volume = Volume(velocity=velocity)
    part.append(c)


def append_rest(part, duration):
    part.append(Rest(quarterLength=duration))


def get_random_part(length, random_lst):
    part = Part()
    instrument_index = random_lst.rand({'min': 0, 'max': len(INSTRUMENTS_CLASSES) - 1})
    instrument_class = INSTRUMENTS_CLASSES[instrument_index]
    set_instrument(part, instrument_class())
    for _ in range(length):
        notePred = random_lst.rand({'min': 0, 'max': 1}, isInt=False)
        duration = random_lst.rand(DURATION, isInt=False)
        isNote = notePred > 0.2
        if isNote:
            num_of_notes = random_lst.rand(NUM_OF_NOTES)
            velocity = random_lst.rand(VELOCITY)
            notes = []
            for _ in range(num_of_notes):
                note = random_lst.rand(PITCH)
                notes.append(note)
            append_chord(part, notes, duration, velocity)
        else:
            append_rest(part, duration)
    return part


class RandomList(object):
    def __init__(self, lst):
        self.lst = lst
        self.index = 0

    def rand(self, minMaxDict, isInt=True):
        val = self.lst[self.index] * (minMaxDict['max'] - minMaxDict['min']) + minMaxDict['min']
        self.index += 1
        if isInt:
            return int(round(val))
        return val


def get_midi_functions():
    # item is music21.stream.Stream
    functions = {}

    def path_to_item(path):
        return translate.midiFilePathToStream(path)

    def item_to_features(item):
        f = features.base.allFeaturesAsList(item)
        return flatten(f[0] + f[1])

    def genome_to_item(genome):
        random_lst = RandomList(genome)
        length = random_lst.rand(LENGTH)
        num_of_parts = random_lst.rand(NUM_OF_PARTS)
        parts = []
        for _ in range(num_of_parts):
            parts.append(get_random_part(length, random_lst))

        stream = Stream(parts)
        return stream

    def save_item(item, save_path):
        midi_file = translate.streamToMidiFile(item)
        binfile = open(save_path, 'wb')
        binfile.write(midi_file.writestr())
        binfile.close()

    functions['path_to_item'] = path_to_item
    functions['item_to_features'] = item_to_features
    functions['genome_to_item'] = genome_to_item
    functions['save_item'] = save_item

    return functions


def main():
    home_folder = "/home/ido"
    type_params = {
        'type_folder': "/Music",
        'type_name': "music",
        'file_extension': "mid"
    }
    names = {'product_name': 'midi_test',
             'data_name': 'midi_test',
             'detector_name': 'midi_test',
             'train_name': 'midi_test'
             }
    functions = get_midi_functions()

    executions_args = []
    executions_args.append(
        {
            'home_folder': home_folder,

            'params': {'population_size': 10, 'num_of_generations': 1, 'genome_size': GENOME_SIZE},
            'flags': {'setup': False, 'verbose': True},
            'names': names,
            'type_params': type_params,

            'functions': functions
        })

    executions_args.append(
        {
            'home_folder': home_folder,

            'params': {'population_size': 100, 'num_of_generations': 10, 'genome_size': GENOME_SIZE},
            'flags': {'setup': False, 'verbose': True},
            'names': names,
            'type_params': type_params,

            'functions': functions
        })

    executions_args.append(
        {
            'home_folder': home_folder,

            'params': {'population_size': 100, 'num_of_generations': 10, 'genome_size': GENOME_SIZE},
            'flags': {'setup': False, 'verbose': True},
            'names': names,
            'type_params': type_params,

            'functions': functions
        })

    src.intelligent_logic.generic_main(executions_args)


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
random list should be part of the lib
'''
