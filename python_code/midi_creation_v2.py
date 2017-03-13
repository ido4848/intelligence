import music21
from pyevolve import G1DList, Initializators, Mutators
import src.intelligent_logic

from music21.stream import Part, Stream
from music21.chord import Chord
from music21.note import Note, Rest
from music21.duration import Duration
from music21 import instrument
from music21.volume import Volume
from music21.midi.realtime import StreamPlayer
import inspect

'''
functions should contain
def path_to_item(path)
def item_to_features(item)
def genome_to_item(genome)
def save_item(item, save_path)
def get_item_genome()
'''


def flatten(l): return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]


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
    functions = {}

    # item is music21.stream.Stream

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

    BLA = 0

    def path_to_item(path):
        return music21.midi.translate.midiFilePathToStream(path)

    def item_to_features(item):
        f = music21.features.base.allFeaturesAsList(item)
        return flatten(f[0] + f[1])

    def get_item_genome():
        # Genome instance

        genome = G1DList.G1DList(GENOME_SIZE)
        genome.setParams(rangemin=0, rangemax=1)

        # Change the initializator to Real values
        genome.initializator.set(Initializators.G1DListInitializatorReal)

        # Change the mutator to Gaussian Mutator
        genome.mutator.set(Mutators.G1DListMutatorRealGaussian)
        return genome

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

    def genome_to_item(genome):
        random_lst = RandomList(genome.genomeList)
        length = random_lst.rand(LENGTH)
        num_of_parts = random_lst.rand(NUM_OF_PARTS)
        parts = []
        for _ in range(num_of_parts):
            parts.append(get_random_part(length, random_lst))

        stream = Stream(parts)
        return stream

    def save_item(item, save_path):
        midi_file = music21.midi.translate.streamToMidiFile(item)
        binfile = open(save_path, 'wb')
        binfile.write(midi_file.writestr())
        binfile.close()

        for el in item.recurse():
            print el

    functions['path_to_item'] = path_to_item
    functions['item_to_features'] = item_to_features
    functions['genome_to_item'] = genome_to_item
    functions['save_item'] = save_item
    functions['get_item_genome'] = get_item_genome

    return functions


def main():
    '''
    home_folder : /home/ido
    type_folder : /Music
    file_extension
    functions

    data_name: midi_compcat_beethoven
    iterations
    freq_stats
    setup
    verbose
    '''

    home_folder = "/home/ido"
    type_folder = "/Music"
    type_name = "music"
    file_extension = "mid"
    functions = get_midi_functions()

    data_name = "midi_test"
    train_name = "midi_test"
    executions_args = []
    executions_args.append(
        {'iterations': 1, 'freq_stats': 1, 'setup': False, 'data_name': data_name, 'train_name': train_name,
         'verbose': True})
    executions_args.append(
        {'iterations': 5, 'freq_stats': 1, 'setup': False, 'data_name': data_name, 'train_name': train_name,
         'verbose': True})
    executions_args.append(
        {'iterations': 10, 'freq_stats': 1, 'setup': False, 'data_name': data_name, 'train_name': train_name,
         'verbose': True})
    src.intelligent_logic.generic_type_main(executions_args, home_folder, type_name, type_folder, file_extension, functions)


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
'''
