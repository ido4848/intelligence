# -*- coding: utf-8 -*-
import sys
import fnmatch
import os
from music_db import Segmented_Music_DB


def collect_file_paths(folder, file_extension_regex):
    file_paths = []
    for root, _, file_names in os.walk(folder):
        for file_name in fnmatch.filter(file_names,'*.' + file_extension_regex):
            file_paths.append(root + "/" + file_name)
    return file_paths

def main():
    FRAME_RATE = 44100
    CHANNELS = 2

    if len(sys.argv) != 4:
        print "Bad usage! usage is {} " \
            "<music-folder-path> <duration_in_seconds>" \
            " <music-db-folder>".format(sys.argv[0])
        return

    music_folder = sys.argv[1]
    duration_seconds = int(sys.argv[2])
    db_name = sys.argv[3]

    mp3_song_files = collect_file_paths(music_folder, "[Mm][Pp]3")
    wav_song_files = collect_file_paths(music_folder, "[Ww][Aa][Ww]")

    print "There were {} suitable songs".format(len(mp3_song_files) + len(wav_song_files))

    db = Segmented_Music_DB.create_new(db_name, FRAME_RATE, CHANNELS, duration_seconds)
    with db.open() as opened_db:
        for mp3_song_file in mp3_song_files:
            try:
                opened_db.add_song(mp3_song_file, "mp3")
            except:
                print "Error inserting mp3 song file {}".format(mp3_song_file)

        for wav_song_file in wav_song_files:
            try:
                opened_db.add_song(wav_song_file, "wav")
            except:
                print "Error inserting wav song file {}".format(wav_song_file)

if __name__ == "__main__":
    main()
