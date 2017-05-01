import inspect
import sys
import os
import numpy as np
from music21 import instrument
from music21.chord import Chord
from music21.duration import Duration
from music21.midi import translate
from music21.note import Rest
from music21.stream import Part, Stream
from music21.volume import Volume
from music21 import features

from intelligence.utilization.general_utilities.caring import apply_carefully


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
    # trick for getting music21 shut up
    _stderr = sys.stderr
    with open(os.devnull, 'w') as f:
        sys.stderr = f
        binfile.write(midi_file.writestr())
    sys.stderr = _stderr
    binfile.close()


def load_midi(path):
    return translate.midiFilePathToStream(path)


def midi_to_feature_list(stream):
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
    feature_lists = apply_carefully(midis, midi_to_feature_list, verbose)
    train_list = np.array(feature_lists)
    return train_list,
