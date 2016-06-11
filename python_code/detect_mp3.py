# -*- coding: utf-8 -*-
from sklearn import svm
import numpy as np
import sys
import pydub
import lsanomaly
from featured_music_db import FeaturedMusicDB


def main():
    if len(sys.argv) != 3:
        print "Bad usage! usage is {} " \
            "<music-db-folder> <mp3-test-path>".format(sys.argv[0])
        return

    music_db_folder = sys.argv[1]
    test_path = sys.argv[2]

    db = FeaturedMusicDB.from_existing(music_db_folder)
    songs = []
    feature_extractor = None
    with db.open() as odb:
        songs = odb.get_all_songs()
        feature_extractor = odb.get_extractor()

    train_data = [song.features for song in songs]


    print "Train data is of size {}".format(len(train_data))
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1) # Todo: switch back?
    # clf = svm.SVC()
    # clf = lsanomaly.LSAnomaly()
    print train_data
    clf.fit(np.array(train_data))


    test_song = pydub.AudioSegment.from_mp3(test_path) 
    test_data = feature_extractor.extract(test_song)

    print 
    print test_data
    pred = clf.predict(np.array([test_data])) # TODO: better predication method

    print pred

if __name__ == "__main__":
    main()
