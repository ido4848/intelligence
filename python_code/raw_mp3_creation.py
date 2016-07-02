import os
import random
import string

import pydub
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


def get_mp3_functions(duration_seconds):
    frame_rate = 44100
    channels = 2
    sample_width = 2

    nframes = frame_rate * channels * sample_width * duration_seconds

    functions = {}

    def path_to_item(path):
        return pydub.AudioSegment.from_mp3(path)

    def item_to_features(item):
        raw_data_list = list(item.raw_data)
        half = len(raw_data_list) / 2
        return [ord(c) for c in raw_data_list][half:half + 5]

    def genome_to_item(genome):
        raw_song = genome.genomeList
        raw_song = ''.join([chr(c) for c in raw_song])
        name = ''.join([random.choice(string.ascii_letters) for _ in range(30)]) + ".raw"
        with open(name, "wb") as f:
            f.write(raw_song)
        song_object = pydub.AudioSegment.from_raw(name, channels=channels, frame_rate=frame_rate,
                                                  sample_width=sample_width)
        os.remove(name)
        return song_object

    def save_item(item, save_path):
        item.export(save_path, "mp3")

    def get_item_genome():
        genome = G1DList.G1DList(nframes)

        # Sets the range max and min of the 1D List
        genome.setParams(rangemin=0, rangemax=255)
        return genome

    functions['path_to_item'] = path_to_item
    functions['item_to_features'] = item_to_features
    functions['genome_to_item'] = genome_to_item
    functions['save_item'] = save_item
    functions['get_item_genome'] = get_item_genome

    return functions


def mp3_main():
    positive_folder = "/home/ido4848/Music/train/mp3_train_old"
    iterations = 3
    freq_stats = 1
    item_path = "/home/ido4848/Music/created_new_mp3.mp3"
    data_path = None  # "/home/ido4848/DB/mp3_old_train"
    duration_seconds = 12
    functions = get_mp3_functions(duration_seconds)
    verbose = True
    setup = True

    src.intelligent_logic.main_logic(functions, positive_folder, iterations, freq_stats, item_path,
                                     data_path=data_path, setup=setup, verbose=verbose)


def main():
    mp3_main()


if __name__ == "__main__":
    main()
