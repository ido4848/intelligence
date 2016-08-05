import math
import random
import sys
import os

import music21
from pyevolve import G1DList
import src.intelligent_logic

'''
functions should contain
def path_to_item(path)
def item_to_features(item)
def genome_to_item(genome)
def save_item(item, save_path)
def get_item_genome()
'''
'''
48 do
50 re
52 mi
53 fa
55 sol
57 la 
59 si
60 do

'''

def flatten(l): return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]


def split_list_to_list_list(lst, tuple_len):
    lst_lst = []
    lst_obj = []
    for i in range(len(lst)):            
        lst_obj.append(lst[i]) 

        if (i + 1) % tuple_len == 0:
            lst_lst.append(lst_obj)
            lst_obj = []

    return lst_lst


#TODO: refactor
def get_midi_level2_functions(base_note, note_count):
    functions = {}

    # item is music21.stream.Stream

    def path_to_item(path):
        return music21.midi.translate.midiFilePathToStream(path)

    def item_to_features(item):
        f = music21.features.base.allFeaturesAsList(item)
        return flatten(f[0] + f[1])

    def get_item_genome():
        genome = G1DList.G1DList(4 * note_count)

        # Sets the range max and min of the 1D List
        genome.setParams(rangemin=1, rangemax=15)
        return genome

    functions['rangemin'] = 1
    functions['rangemax'] = 15
    functions['genomelistlength'] = 5 * note_count
    '''
    0: duration
    1-3: pithches
    '''
    def genome_list_to_sound_list(genome_list):
        return split_list_to_list_list(genome_list, 5)


    def scale_mapping(base_note, index):
        scale_lst = [0 ,2, 4, 5, 7, 9, 11, 12]
        return base_note + scale_lst[index - 1]

    def pitch_lst_mapping(raw_pitch_lst):
        pitch_lst = []

        count = 0
        for pitch in raw_pitch_lst:
            pitch = pitch - 7
            if pitch > 0 and pitch < 9:
                pitch_lst.append(scale_mapping(base_note, pitch))
                count += 1
        if count == 0:
            pitch_lst.append(base_note + int(math.fabs(raw_pitch_lst[0] - 7)))
        return pitch_lst


    def duration_mapping(raw_duration):
        if raw_duration % 5 == 0:
            return 0.25

        if raw_duration % 5 == 1:
            return 0.5

        if raw_duration % 5 == 2:
            return 0.5

        if raw_duration % 5 == 3:
            return 1

        if raw_duration % 5 == 4:
            return 2

    '''
    0: duration
    1: list of pitches
    '''
    def sound_mapping(sound_lst):
        sound_lst[0] = duration_mapping(sound_lst[0])
        sound_lst[1] = pitch_lst_mapping(sound_lst[1::])
        return [sound_lst[0], sound_lst[1]]

    def sound_list_to_item(sound_list):        
        stream = music21.stream.Stream()
        tempo = 120  # TODO:?

        for sound_obj in sound_list:
            sound_obj = sound_mapping(sound_obj)
            duration = music21.duration.Duration(sound_obj[0])
            chord = music21.chord.Chord(sound_obj[1], duration=duration)
            stream.append(chord)

        return stream

    def genome_to_item(genome):
        return genome_list_to_item(genome.genomeList)

    def genome_list_to_item(genome_list):
        sound_list = genome_list_to_sound_list(genome_list)
        return sound_list_to_item(sound_list)

    def save_item(item, save_path):
        midi_file = music21.midi.translate.streamToMidiFile(item)
        binfile = open(save_path, 'wb')
        binfile.write(midi_file.writestr())
        binfile.close()

        mp3_path = save_path + ".mp3"
        os.system('rm {}'.format(mp3_path))
        os.system("timidity {} -Ow -o - | ffmpeg -i - -acodec libmp3lame -ab 64k {}".format(save_path, mp3_path))  


    functions['path_to_item'] = path_to_item
    functions['item_to_features'] = item_to_features
    functions['genome_to_item'] = genome_to_item
    functions['save_item'] = save_item
    functions['get_item_genome'] = get_item_genome
    functions['genome_list_to_item'] = genome_list_to_item

    return functions

def get_midi_functions(duration_seconds):
    tempo = 120
    note_count = tempo * duration_seconds / 60

    functions = {}

    # item is music21.stream.Stream

    def path_to_item(path):
        return music21.midi.translate.midiFilePathToStream(path)

    def item_to_features(item):
        f = music21.features.base.allFeaturesAsList(item)
        return flatten(f[0] + f[1])

    def genome_to_item(genome):
        pitch_lst = genome.genomeList
        mt = music21.midi.MidiTrack(1)
        stream = music21.stream.Stream()
        track = 0
        time = 0
        channel = 0
        duration = 1
        quarter_duration = 1024
        volume = 100
        tempo = 120  # TODO:?

        for pitch in pitch_lst:
            dt1 = music21.midi.DeltaTime(mt)
            dt1.time = time * quarter_duration

            me_on = music21.midi.MidiEvent(mt)
            me_on.type = "NOTE_ON"
            me_on.pitch = pitch
            me_on.velocity = volume

            dt2 = music21.midi.DeltaTime(mt)
            dt2.time = (time + duration) * quarter_duration

            me_off = music21.midi.MidiEvent(mt)
            me_off.type = "NOTE_OFF"
            me_off.pitch = pitch
            me_off.velocity = 0

            note = music21.midi.translate.midiEventsToNote([dt1, me_on, dt2, me_off])
            time += duration
            stream.append(note)

        return stream

    def save_item(item, save_path):
        midi_file = music21.midi.translate.streamToMidiFile(item)
        binfile = open(save_path, 'wb')
        binfile.write(midi_file.writestr())
        binfile.close()

    def get_item_genome():
        genome = G1DList.G1DList(note_count)

        # Sets the range max and min of the 1D List
        genome.setParams(rangemin=30, rangemax=70)
        return genome

    functions['path_to_item'] = path_to_item
    functions['item_to_features'] = item_to_features
    functions['genome_to_item'] = genome_to_item
    functions['save_item'] = save_item
    functions['get_item_genome'] = get_item_genome
    functions['rangemin'] = 30
    functions['rangemax'] = 70

    return functions


def midi_main(duration_seconds, iterations, freq_stats, positive_folder, data_path, detector_path, item_path, setup=False,
              verbose=True):
    functions = get_midi_functions(duration_seconds)
    src.intelligent_logic.main_logic(functions, positive_folder, iterations, freq_stats, item_path,
                                     data_path=data_path, detector_path=detector_path, setup=setup, verbose=verbose)

def midi_level2_main(base_note, note_count, iterations, freq_stats, positive_folder, data_path, detector_path, item_path, setup=False,
              verbose=True):
    functions = get_midi_level2_functions(base_note, note_count)
    src.intelligent_logic.main_logic(functions, positive_folder, iterations, freq_stats, item_path,
                                     data_path=data_path, detector_path=detector_path, setup=setup, verbose=verbose)

def create_one(note_count, item_path):
    functions = get_midi_level2_functions(51, note_count)
    random_list = [random.randrange(functions['rangemin'],functions['rangemax']) for _ in range(functions['genomelistlength'])]
    item = functions['genome_list_to_item'](random_list)
    functions['save_item'](item, item_path)


def test_main():
    train_folder = "/home/ido4848/Music/train/midi_train"
    db_path = "/home/ido4848/DB/midi_test_data"
    detector_path = "/home/ido4848/DB/midi_test_data_detector"
    product_folder = "/home/ido4848/Music"


    midi_level2_main(10, 1, 1  , train_folder, db_path, detector_path,
              product_folder + "/test_created_midi_level2_6.mid", setup=False)

def pro_main():
    train_folder = "/home/ido4848/Music/train/midi_classical_train"
    db_path = "/home/ido4848/DB/midi_classical_data_some2"
    detector_path = "/home/ido4848/DB/midi_classical_data_some2_detector"
    product_folder = "/home/ido4848/Music"


    midi_level2_main(58, 50, 5000, 50, train_folder, db_path, detector_path,
              product_folder + "/classical_created_midi_level2_13.mid", setup=False)


if __name__ == "__main__":
    pro_main()

    '''
    if sys.argv[1] == '1':
        create_one(15, "/home/ido4848/Music/test_midi_level2_2.mid")
    elif sys.argv[1] == '2':
        test_main()
    '''