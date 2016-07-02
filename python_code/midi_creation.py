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
        genome.setParams(rangemin=20, rangemax=100)
        return genome

    functions['path_to_item'] = path_to_item
    functions['item_to_features'] = item_to_features
    functions['genome_to_item'] = genome_to_item
    functions['save_item'] = save_item
    functions['get_item_genome'] = get_item_genome

    return functions


def midi_main(duration_seconds, iterations, freq_stats, positive_folder, data_path, item_path, setup=False,
              verbose=True):
    functions = get_midi_functions(duration_seconds)
    src.intelligent_logic.main_logic(functions, positive_folder, iterations, freq_stats, item_path,
                                     data_path=data_path, setup=setup, verbose=verbose)


def main():
    midi_main(5, 3, 1, "/home/ido4848/Music/train/midi_classical_train", "/home/ido4848/DB/midi_classical_data",
              "/home/ido4848/Music/classical_created_midi_1.mid", setup=True)

    midi_main(15, 30, 5, None, "/home/ido4848/DB/midi_classical_data",
              "/home/ido4848/Music/classical_created_midi_2.mid", setup=False)

    midi_main(30, 50, 10, None, "/home/ido4848/DB/midi_classical_data",
              "/home/ido4848/Music/classical_created_midi_3.mid", setup=False)

    midi_main(30, 100, 20, None, "/home/ido4848/DB/midi_classical_data",
              "/home/ido4848/Music/classical_created_midi_4.mid", setup=False)

    midi_main(60, 100, 20, None, "/home/ido4848/DB/midi_classical_data",
              "/home/ido4848/Music/classical_created_midi_5.mid", setup=False)

    midi_main(60, 200, 20, None, "/home/ido4848/DB/midi_classical_data",
              "/home/ido4848/Music/classical_created_midi_6.mid", setup=False)

    midi_main(60, 500, 50, None, "/home/ido4848/DB/midi_classical_data",
              "/home/ido4848/Music/classical_created_midi_6.mid", setup=False)

    midi_main(100, 1000, 100, None, "/home/ido4848/DB/midi_classical_data",
              "/home/ido4848/Music/classical_created_midi_6.mid", setup=False)


if __name__ == "__main__":
    main()

