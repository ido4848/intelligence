# -*- coding: utf-8 -*-
from sklearn import svm
import numpy as np
import pickle
import sys
import pydub
import os
from sklearn.externals import joblib


def restore_music_db(db_name):
    return joblib.load(db_name + "/dbfile.pkl") 


def store_detector(clf_name, clf):
    if not os.path.exists(clf_name):
        os.makedirs(clf_name)

    joblib.dump(clf, clf_name + "/clffile.pkl", compress=5)


def main():
    if len(sys.argv) != 3:
        print "Bad usage! usage is {} " \
            "<music-db-name> <classifier-name>".format(sys.argv[0])
        return

    db_name = sys.argv[1]
    clf_name = sys.argv[2]

    songs = restore_music_db(db_name)
    print "There are {} songs in the db {}".format(len(songs), db_name)


    raw_song_arrays = [list(song.raw_data) for song in songs]
    train_data = [[ord(c) for c in raw_array] for raw_array in raw_song_arrays]

    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
    clf.fit(train_data)

    store_detector(clf_name, clf)

if __name__ == "__main__":
    main()
