# -*- coding: utf-8 -*-
import sys
import pydub
from pydub.playback import play
import os
import shelve
import re
import random
import feature_extractors


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
              self).__init__("DB " + str(db_folder) + " is not open!")


class SoundFormatNotSupported(Exception):
    def __init__(self, format):
        # Call the base class constructor with the parameters it needs
        super(SoundFormatNotSupported, self).__init__(
            "Sound format " + str(format) + " is not supported.")


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
        self._matching_predicate = self._db_instance["_matching_predicate"]
        self._index_counter = self._db_instance["_index_counter"]
        self._feature_extractor = self._db_instance["_feature_extractor"]
        self.close()

        return self

    @staticmethod
    def create_new(db_folder, matching_predicate, feature_extractor):
        self = FeaturedMusicDB()

        self._folder = db_folder
        self._path = self._folder + "/" + "dbfile.pkl"
        if not os.path.exists(self._folder):
            os.makedirs(self._folder)

        self._matching_predicate = matching_predicate
        self._index_counter = 0
        self._feature_extractor = feature_extractor

        self._db_instance = None
        self.open()
        self._db_instance["_matching_predicate"] = self._matching_predicate
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
        midi_regex = re.compile("[Mm][Ii][Dd]([Ii])?")
        if wav_regex.match(file_format) is not None:
            return pydub.AudioSegment.from_wav(song_file_path), "pydub"
        elif mp3_regex.match(file_format) is not None:
            return pydub.AudioSegment.from_mp3(song_file_path), "pydub"
        elif midi_regex.match(file_format) is not None:
           raise NotImplementedError()
        else:
            raise SoundFormatNotSupported(file_format)

    def add_mp3s(self, mp3_song_files):
        for mp3_song_file in mp3_song_files:
            try:
                self.add_song(mp3_song_file, "mp3")
            except Exception as e:
                print "Error inserting mp3 song file {}: {}".format(mp3_song_file, e.args)

    def add_wavs(self, wav_song_files):
        for wav_song_file in wav_song_files:
            try:
                self.add_song(wav_song_file, "wav")
            except Exception as e:
                print "Error inserting mp3 song file {}: {}".format(wav_song_file, e.message)

    def add_song(self, song_file_path, file_format):
        if self._db_instance is None:
            raise DBNotOpen(self._folder)

        song, song_object_format = self._open_song(song_file_path, file_format)
        if not self._matching_predicate(song, song_object_format):
            raise Exception("Song does not match db format")

        try:
            features = self._feature_extractor.extract(song, song_object_format)
        except Exception as e:
            print "Error during extracting features from {}:{}".format(song_file_path, e.message)
            return

        self._index_counter += 1

        self._db_instance[str(self._index_counter)] = Song(song_file_path, file_format, [], features)
        self._db_instance["_index_counter"] = self._index_counter

        return self._index_counter

    def remove_song(self, song_counter):
        song_counter = str(song_counter)
        if self._db_instance is None:
            raise DBNotOpen(self._folder)

        if song_counter not in self._db_instance:
            raise SongNotFound()

        self._db_instance[song_counter] = None
        del self._db_instance[song_counter]

    def get_song(self, song_counter):
        song_counter = str(song_counter)
        if self._db_instance is None:
            raise DBNotOpen(self._folder)

        if song_counter not in self._db_instance:
            raise SongNotFound()

        return self._db_instance[song_counter]

    def get_all_songs(self):
        items = self._db_instance.items()
        songs = []
        for item in items:
            if type(item[1]) == type(Song("", "", "", "")):
                songs += [item[1]]
        return songs

    def get_extractor(self):
        return self._feature_extractor


def play_music_from_db(db_folder, count):
    db = FeaturedMusicDB.from_existing(db_folder)
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
    if len(sys.argv) == 3:
        play_music_from_db(sys.argv[1], int(sys.argv[2]))

    else:
        print "Not a valid number of parameters"
        return


if __name__ == "__main__":
    main()
