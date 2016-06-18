import pydub
from pyevolve import G1DList
import music_creation
import music_detection


def raw_main_logic(music_detector, duration_seconds, iterations, song_path, song_format):
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
        return song_object

    creator = music_creation.music_creator.MusicCreator(music_detector, genome, to_song_object)
    best_genome = creator.create(iterations)
    best_song = to_song_object(best_genome)
    best_song.export(song_path, song_format)


def main():
    setup = False
    if raw_input("setup(True/False): ") in ['true', 'True', "TRUE", 't', 'y', 'yes', 'Y', '1']:
        setup = True
    test_folders = [(0.5, "/home/ido4848/Music/mp3s/train"), (-0.5, "/home/ido4848/Music/mp3s/negative_test"),
                    (0.5, "/home/ido4848/Music/mp3s/positive_test")]
    music_detector = music_detection.main_detection.get_detector("/home/ido4848/Music/mp3s/train",
                                                                 "/home/ido4848/DB/raw_songs", setup=setup)
    raw_main_logic(music_detector, 15, 5, "~/Music/created1.mp3", "mp3")


if __name__ == "__main__":
    main()
