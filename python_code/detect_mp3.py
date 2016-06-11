# -*- coding: utf-8 -*-
from sklearn import svm
import numpy as np
import sys
import pydub
import lsanomaly
from featured_music_db import FeaturedMusicDB

def detect_mp3(db_name, test_path):
    db = FeaturedMusicDB.from_existing(db_name)
    songs = []
    feature_extractor = None
    with db.open() as odb:
        songs = odb.get_all_songs()
        feature_extractor = odb.get_extractor()

    train_data = [song.features for song in songs]


    # print "Train data is of size {}".format(len(train_data))
    clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1) # Todo: switch back?
    # clf = svm.SVC()
    # clf = lsanomaly.LSAnomaly()
    clf.fit(np.array(train_data))


    test_song = pydub.AudioSegment.from_mp3(test_path) 
    test_data = feature_extractor.extract(test_song)

    pred = clf.predict(np.array([test_data])) # TODO: better predication method

    print "pred for {} is {}".format(test_path, pred)

def main():
    if len(sys.argv) != 3:
        print "Bad usage! usage is {} " \
            "<music-db-folder> <mp3-test-path>".format(sys.argv[0])
        return

    music_db_folder = sys.argv[1]
    test_path = sys.argv[2]

    detect_mp3(db_name, test_path)




if __name__ == "__main__":
    main()
