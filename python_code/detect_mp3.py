# -*- coding: utf-8 -*-
from sklearn import svm
import numpy as np
import sys
import pydub
from music_db import Segmented_Music_DB


def main():
    if len(sys.argv) != 3:
        print "Bad usage! usage is {} " \
            "<music-db-folder> <mp3-sample-path>".format(sys.argv[0])
        return

    music_db_folder = sys.argv[1]
    sample_path = sys.argv[2]

    db = Segmented_Music_DB.from_existing(music_db_folder)
    song_segments = []
    duration_seconds = 0
    with db.open() as odb:
        song_segments = odb.get_all_song_segments()
        duration_seconds = odb._db_instance["_duration_seconds"]

    raw_song_arrays = [list(song.raw_data) for song in song_segments]
    train_data = [[ord(c) for c in raw_array] for raw_array in raw_song_arrays]
    train_type = [1 for _ in range(len(train_data))]

    print "Train data is of size {}".format(len(train_data))
    # clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1) # Todo: switch back?
    clf = svm.SVC()

    train_data.append([0 for _ in range(len(train_data[0]))]) # TODO: append here real sound?
    train_type += [0]
    clf.fit(np.array(train_data), np.array(train_type))

    sample = pydub.AudioSegment.from_mp3(sample_path)
    print sample.frame_rate
    sample_cut = sample[0:1000 * duration_seconds:]
    sample_cut_array = list(sample_cut.raw_data)
    sample_cut_test = [ord(c) for c in sample_cut_array] 
    pred = clf.predict(np.array([sample_cut_test])) # TODO: better predication method

    if pred[0] == 1:
        print "Sample {} is music!".format(sample_path)
    else:
        print "Sample {} is not music!".format(sample_path)

if __name__ == "__main__":
    main()
