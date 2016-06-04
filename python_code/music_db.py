# -*- coding: utf-8 -*-
import sys
import pydub
import fnmatch
import os
import shelve
import re


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
        super(SongNotFound, self).__init__(
            "DB " +str(db_folder) + " is not open!")


class SoundFormatNotSupported(Exception):
    def __init__(self, format):

        # Call the base class constructor with the parameters it needs
        super(SoundFormatNotSupported, self).__init__(
            "Sound format " +str(format) + " is not supported.")


class Segmented_Music_DB(object):
    def __init__(self, db_folder, frame_rate, channels, duration_seconds):
        self._folder = db_folder
        self._path = self._folder + "/" + "dbfile.pkl"
        if not os.path.exists(self._folder):
            os.makedirs(self._folder)

        self._frame_rate = frame_rate
        self._channels = channels
        self._duration_seconds = duration_seconds

        self._db_instance = None
        self.open()
        self.close()

    def open(self):
        return self.__enter__()

    def close(self):
        self.__exit__("","","")

    def __enter__(self):
        if self._db_instance is None:
            self._db_instance = shelve.open(self._path)
        return self

    def __exit__(self, type, value, traceback):
        if self._db_instance is not None:
            self._db_instance.close()
            self._db_instance = None

    def _open_song(self, song_file, file_format):
        wav_regex = re.compile("[Ww][Aa][Vv]([Ee])?")
        mp3_regex = re.compile("[Mm][Pp]3")
        if wav_regex.match(file_format) is not None:
            return pydub.AudioSegment.from_wav(song_file)
        elif mp3_regex.match(file_format) is not None:
            return pydub.AudioSegment.from_mp3(song_file)
        else:
            raise SoundFormatNotSupported(file_format)

    def _does_song_match(self, song):
        return song.frame_rate == self._frame_rate and song.channels == self._channels

    def _split_song(self, song):
        offset = 0
        duration = self._duration_seconds * 1000
        song_segments = []
        while offset + duration < song.duration_seconds * 1000:
            song_segments.append(song[offset:offset + duration])
            offset = offset + duration
        if duration < song.duration_seconds:
            song_segments.append(song[-duration])

        return song_segments

    def add_song(self, song_name, song_file, file_format):
        if self._db_instance is None:
            raise DBNotOpen(self._folder)

        if song_name in self._db_instance:
            raise SongAlreadyExists()

        song = self._open_song(song_file, file_format)
        if not self._does_song_match(song):
            raise Exception("Song " + song_name + "does not match db format")

        song_segments = self._split_song(song)
        self._db_instance[song_name] = song_segments

    def remove_song(self, song_name):
        if self._db_instance is None:
            raise DBNotOpen(self._folder)

        if song_name not in self._db_instance:
            raise SongNotFound()

        self._db_instance[song_name] = None
        del self._db_instance[song_name]

    def get_song_segments(self, song_name):
        if self._db_instance is None:
            raise DBNotOpen(self._folder)

        if song_name not in self._db_instance:
            raise SongNotFound()

        return self._db_instance[song_name]


def main():
    FRAME_RATE = 44100
    CHANNELS = 2

    if len(sys.argv) != 3:
        print "Bad usage! usage is {} " \
            "<db-folder-path> <duration_in_seconds>" \
            "".format(sys.argv[0])
        return

    db = Segmented_Music_DB(sys.argv[1], FRAME_RATE, CHANNELS, int(sys.argv[2]))     
    with db.open() as opened_db:
        print opened_db
        opened_db.add_song("test_song","i.mp3","mp3")
        segments = opened_db.get_song_segments("test_song")
        print "Song was segmented to {} parts".format(len(segments))
        opened_db.remove_song("test_song")

if __name__ == "__main__":
    main()
