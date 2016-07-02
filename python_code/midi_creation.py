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


def flatten(l): return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]


def get_midi_functions(duration_seconds):
    tempo = 120
    min = 20
    max = 100
    note_count = tempo * duration_seconds / 60

    functions = {}

    # item is music21.midi.Stream

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
        genome.setParams(rangemin=20, rangemax=100)
        return genome

    functions['path_to_item'] = path_to_item
    functions['item_to_features'] = item_to_features
    functions['genome_to_item'] = genome_to_item
    functions['save_item'] = save_item
    functions['get_item_genome'] = get_item_genome

    return functions


def midi_main():
    positive_folder = "/home/ido4848/Music/train/midi_train"
    iterations = 3
    freq_stats = 1
    item_path = "/home/ido4848/Music/create_midi_3.mid"
    detector_path = None  # TODO: A BUG HERE
    duration_seconds = 7
    functions = get_midi_functions(duration_seconds)
    verbose = True
    setup = True

    src.intelligent_logic.main_logic(functions, positive_folder, iterations, freq_stats, item_path,
                                                detector_path=detector_path, setup=setup, verbose=verbose)


def main():
    midi_main()


if __name__ == "__main__":
    main()

'''

def main():
    setup = False
    if raw_input("setup(True/False): ") in ['true', 'True', "TRUE", 't', 'y', 'yes', 'Y', '1']:
        setup = True

    train_folder = "/home/ido4848/Music/mp3s/train/The top 100 masterpieces 1685-1928"
    old_train_folder = "/home/ido4848/Music/mp3s/train/old"
    negative_folder = "/home/ido4848/Music/mp3s/negative_test"
    positive_folder = "/home/ido4848/Music/mp3s/positive_test"
    db_folder = "/home/ido4848/DB/classical_100_masterpieces_db_v2"
    old_db_folder = "/home/ido4848/DB/raw_songs_v2"

    test_folders = [(0.5, train_folder), (-0.5, negative_folder), (0.5, positive_folder)]
    music_detector = music_detection.main_detection.get_detector(train_folder,
                                                                 db_folder, setup=setup)
    old_music_detector = music_detection.main_detection.get_detector(old_train_folder,
                                                                     old_db_folder, setup=True)
    # music_detection.main_detection.detection_logic(train_folder, db_folder, test_folders,
    #                                              setup=setup, detector=music_detector)

    single_note_midi_main_logic(music_detector, 100, 150, "/home/ido4848/Music/classic_created150_v2.mp3", "mp3",
                                freq_stats=1)
    single_note_midi_main_logic(old_music_detector, 100, 150, "/home/ido4848/Music/created150.mp3", "mp3",
                                freq_stats=1)
    single_note_midi_main_logic(music_detector, 100, 500, "/home/ido4848/Music/classic_created500.mp3", "mp3",
                                freq_stats=20)
    single_note_midi_main_logic(old_music_detector, 100, 500, "/home/ido4848/Music/created500.mp3", "mp3",
                                freq_stats=1)
    single_note_midi_main_logic(music_detector, 100, 1000, "/home/ido4848/Music/classic_created1000.mp3", "mp3",
                                freq_stats=50)
    single_note_midi_main_logic(old_music_detector, 100, 1000, "/home/ido4848/Music/created1000.mp3", "mp3",
                                freq_stats=1)
    single_note_midi_main_logic(music_detector, 200, 1000, "/home/ido4848/Music/classic_created1000_2.mp3", "mp3",
                                freq_stats=50)
    single_note_midi_main_logic(old_music_detector, 200, 1000, "/home/ido4848/Music/created1000_2.mp3", "mp3",
                                freq_stats=1)
    single_note_midi_main_logic(music_detector, 100, 10000, "/home/ido4848/Music/classic_created10000.mp3", "mp3",
                                freq_stats=200)
    single_note_midi_main_logic(old_music_detector, 100, 10000, "/home/ido4848/Music/created10000.mp3", "mp3",
                                freq_stats=1)
    single_note_midi_main_logic(music_detector, 100, 100000, "/home/ido4848/Music/classic_created100000.mp3", "mp3",
                                freq_stats=1000)
    single_note_midi_main_logic(old_music_detector, 100, 100000, "/home/ido4848/Music/created100000.mp3", "mp3",
                                freq_stats=1)

'''
