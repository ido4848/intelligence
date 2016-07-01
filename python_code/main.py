import pydub
from pyevolve import G1DList
import music_creation
import music_detection
import os


def single_note_midi_main_logic(music_detector, note_count, iterations, song_path, song_format, freq_stats=0):
    genome = G1DList.G1DList(note_count)

    # Sets the range max and min of the 1D List
    genome.setParams(rangemin=40, rangemax=80)

    def to_song_object(raw_g1d_song):
        try:
            os.remove("temp_midi.midi")
        except OSError:
            pass
        try:
            os.remove("temp_midi.wav")
        except OSError:
            pass

        midi_object = music_creation.midi_creation.create_midi_from_pitches(raw_g1d_song.genomeList)
        music_creation.midi_creation.save_midi(midi_object, "temp_midi.midi")
        timidity_command = r"timidity {} -Ow -o {} 1> \dev\null 2> \dev\null ".format("temp_midi.midi", "temp_midi.wav")
        temp = os.system(timidity_command)
        song_object = pydub.AudioSegment.from_wav("temp_midi.wav")
        return song_object, "pydub"

    creator = music_creation.music_creator.MusicCreator(music_detector, genome, to_song_object)
    best_genome = creator.create(iterations, freq_stats=freq_stats)
    print best_genome.genomeList
    best_song, best_song_type = to_song_object(best_genome)
    best_song.export(song_path, song_format)


def raw_main_logic(music_detector, duration_seconds, iterations, song_path, song_format, freq_stats=0):
    frame_rate = 44100
    channels = 2
    sample_width = 2

    nframes = frame_rate * channels * sample_width * duration_seconds
    genome = G1DList.G1DList(nframes)

    # Sets the range max and min of the 1D List
    genome.setParams(rangemin=0, rangemax=255)

    def to_song_object(raw_g1d_song):
        raw_song = raw_g1d_song.genomeList
        raw_song = ''.join([chr(c) for c in raw_song])
        with open("temp.raw", "wb") as f:
            f.write(raw_song)
        song_object = pydub.AudioSegment.from_raw("temp.raw", channels=channels, frame_rate=frame_rate,
                                                  sample_width=sample_width)
        return song_object, "pydub"

    creator = music_creation.music_creator.MusicCreator(music_detector, genome, to_song_object)
    best_genome = creator.create(iterations, freq_stats=freq_stats)
    best_song, best_song_type = to_song_object(best_genome)
    best_song.export(song_path, song_format)


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


def save_midi_from_lst(lst, file_name, file_type):
    midi_object = music_creation.midi_creation.create_midi_from_pitches(lst)
    music_creation.midi_creation.save_midi(midi_object, "temp_midi.midi")
    timidity_command = r"timidity {} -Ow -o {} 1> \dev\null 2> \dev\null ".format("temp_midi.midi", "temp_midi.wav")
    temp = os.system(timidity_command)
    song_object = pydub.AudioSegment.from_wav("temp_midi.wav")
    song_object.export(file_name, file_type)


if __name__ == "__main__":
    main()
