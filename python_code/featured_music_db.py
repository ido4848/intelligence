# -*- coding: utf-8 -*-
import sys
import pydub
from pydub.playback import play
import os
import shelve
import re
import random


class Song(object):
    def __init__(self, file_path, file_format, sample, features):
        self.file_path = file_path
        self.features = features
        self.file_format = file_format
        self.sample = sample


class SongAlreadyExists(Exception):
    def __init__(self):

        # Call the base class constructor with the parameters it needs
        super(SongAlreadyExists, self).__init__("Song already in db!")


class SongNotFound(Exception):
    def __init__(self):

        # Call the base class constructor with the parameters it needs
        super(SongNotFound, self).__init__("Song is not in db!")


class DBNotOpen(Exception):
    def __init__(self, db_folder):

        # Call the base class constructor with the parameters it needs
        super(SongNotFound,
              self).__init__("DB " +str(db_folder) + " is not open!")


class SoundFormatNotSupported(Exception):
    def __init__(self, format):

        # Call the base class constructor with the parameters it needs
        super(SoundFormatNotSupported, self).__init__(
            "Sound format " +str(format) + " is not supported.")


class FeaturedMusicDB(object):
    def __init__(self):
        pass

    @staticmethod
    def from_existing(db_folder):
        self = FeaturedMusicDB()

        self._folder = db_folder
        self._path = self._folder + "/" + "dbfile.pkl"

        self._db_instance = None
        self.open()
        self._channels = self._db_instance["_channels"]
        self._index_counter = self._db_instance["_index_counter"]
        self._feature_extractor = self._db_instance["_feature_extractor"]
        self.close()

        return self

    @staticmethod
    def create_new(db_folder, frame_rate, channels, feature_extractor):
        self = FeaturedMusicDB()

        self._folder = db_folder
        self._path = self._folder + "/" + "dbfile.pkl"
        if not os.path.exists(self._folder):
            os.makedirs(self._folder)

        self._frame_rate = frame_rate
        self._channels = channels
        self._index_counter = 0
        self._feature_extractor = feature_extractor

        self._db_instance = None
        self.open()
        self._db_instance["_channels"] = self._channels
        self._db_instance["_index_counter"] = self._index_counter
        self._db_instance["_feature_extractor"] = self._feature_extractor
        self.close()
        return self

    def open(self):
        return self.__enter__()

    def close(self):
        self.__exit__("", "", "")

    def __enter__(self):
        if self._db_instance is None:
            self._db_instance = shelve.open(self._path)
        return self

    def __exit__(self, type, value, traceback):
        if self._db_instance is not None:
            self._db_instance.close()
            self._db_instance = None

    def _open_song(self, song_file_path, file_format):
        wav_regex = re.compile("[Ww][Aa][Vv]([Ee])?")
        mp3_regex = re.compile("[Mm][Pp]3")
        if wav_regex.match(file_format) is not None:
            return pydub.AudioSegment.from_wav(song_file_path)
        elif mp3_regex.match(file_format) is not None:
            return pydub.AudioSegment.from_mp3(song_file_path)
        else:
            raise SoundFormatNotSupported(file_format)

    def _does_song_match(self, song):
        return song.frame_rate == self._frame_rate and song.channels == self._channels

    def add_song(self, song_file_path, file_format):
        if self._db_instance is None:
            raise DBNotOpen(self._folder)

        song = self._open_song(song_file_path, file_format)
        if not self._does_song_match(song):
            raise Exception("Song does not match db format")

        features = self._feature_extractor.extract(song)

        self._index_counter += 1

        self._db_instance[str(self._index_counter)] =  Song(song_file_path, file_format, [], features)
        self._db_instance["_index_counter"] = self._index_counter

        return self._index_counter

    def remove_song(self, song_counter):
        song_name = str(song_name)
        if self._db_instance is None:
            raise DBNotOpen(self._folder)

        if song_name not in self._db_instance:
            raise SongNotFound()

        self._db_instance[song_name] = None
        del self._db_instance[song_name]

    def get_song(self, song_counter):
        song_name = str(song_name)
        if self._db_instance is None:
            raise DBNotOpen(self._folder)

        if song_name not in self._db_instance:
            raise SongNotFound()

        return self._db_instance[song_name]

    def get_all_songs(self):
        items = self._db_instance.items()
        songs = []
        for item in items:
            if type(item[1]) == type(Song("","","","")):
                songs += [item[1]]
        return songs

    def get_extractor(self):
        return self._feature_extractor


def create_test_db(db_folder, frame_rate, channels, duration_in_seconds, test_song_path):
    db = Featured_Music_DB.create_new(db_folder, frame_rate, channels, duration_in_seconds)
    with db.open() as opened_db:

        index = opened_db.add_song(test_song_path, "mp3")
        print "song was inserted in index {}".format(index)
        opened_db.remove_song(index)
        print "Song indexed {} was removed from db".format(index)

        index = opened_db.add_song(test_song_path, "mp3")
        print "Song was inserted by index with index {}".format(index)
        opened_db.remove_song(index)
        print "Song indexed {} was removed from db".format(index)

        index = opened_db.add_song(test_song_path, "mp3")
        print "Song was inserted by index with index {}".format(index)


def play_music_from_db(db_folder, count):
    db = Featured_Music_DB.from_existing(db_folder)
    with db.open() as odb:
        this_count = 0
        songs = odb.get_all_songs()
        while this_count < count:
            song = random.choice(songs)
            try:
                play(song.sample)
                this_count += 1
            except:
                pass


def main():
    FRAME_RATE = 44100
    CHANNELS = 2

    if len(sys.argv) == 3:
        play_music_from_db(sys.argv[1], int(sys.argv[2]))

    elif len(sys.argv) == 4:
        create_test_db(sys.argv[1], FRAME_RATE, CHANNELS, int(sys.argv[2]), sys.argv[3], )

    else:
        print "Not a valid number of parameters"
        return


if __name__ == "__main__":
    main()
