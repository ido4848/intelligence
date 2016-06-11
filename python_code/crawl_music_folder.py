# -*- coding: utf-8 -*-
import sys
import fnmatch
import os
from featured_music_db import FeaturedMusicDB
import feature_extractors


FRAME_RATE = 44100
CHANNELS = 2

def collect_file_paths(folder, file_extension_regex):
    file_paths = []
    for root, _, file_names in os.walk(folder):
        for file_name in fnmatch.filter(file_names,'*.' + file_extension_regex):
            file_paths.append(root + "/" + file_name)
    return file_paths


def crawl_music_folder(music_folder, db_name):
    mp3_song_files = collect_file_paths(music_folder, "[Mm][Pp]3")
    wav_song_files = collect_file_paths(music_folder, "[Ww][Aa][Ww]")

    extractor = feature_extractors.RawDataFeatureExtractor()

    print "There were {} suitable songs".format(len(mp3_song_files) + len(wav_song_files))

    db = FeaturedMusicDB.create_new(db_name, FRAME_RATE, CHANNELS, extractor)
    with db.open() as opened_db:
        for mp3_song_file in mp3_song_files:
            try:
                opened_db.add_song(mp3_song_file, "mp3")
            except Exception as e:
                print "Error inserting mp3 song file {}: {}".format(mp3_song_file, e.message)

        for wav_song_file in wav_song_files:
            try:
                opened_db.add_song(wav_song_file, "wav")
            except Exception as e:
                print "Error inserting mp3 song file {}: {}".format(mp3_song_file, e.message)


def main():

    if len(sys.argv) != 3:
        print "Bad usage! usage is {} " \
            "<music-folder-path>" \
            " <music-db-folder>".format(sys.argv[0])
        return

    music_folder = sys.argv[1]
    db_name = sys.argv[2]
    crawl_music_folder(music_folder, db_name)

if __name__ == "__main__":
    main()
