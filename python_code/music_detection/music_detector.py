import numpy as np
import sys

import pydub
import sklearn

import featured_music_db


class MusicDetector(object):
    def __init__(self, music_db_folder, regressioner):
        self._music_db_folder = music_db_folder
        self._music_db = featured_music_db.FeaturedMusicDB.from_existing(self._music_db_folder)
        self._regressioner = regressioner
        self._feature_extractor = None

        self._fit()

    def _fit(self):
        songs = []
        with self._music_db.open() as odb:
            songs = odb.get_all_songs()
            self._feature_extractor = odb.get_extractor()

        train_data = [song.features for song in songs]

        try:
            self._regressioner.fit(np.array(train_data))
            return
        except Exception as e:
            print "Error in fitting regressioner: {}".format(e.message)

        try:
            train_tags = [1 for _ in range(len(train_data))]
            self._regressioner.fit(np.array(train_data), np.array(train_tags))
            return
        except Exception as e:
            print "Error in fitting regressioner(using tags): {}".format(e.message)

        try:
            self._regressioner.fit(np.array(train_data), 1)
        except Exception as e:
            print "Error in fitting regressioner(using one tag): {}".format(e.message)

    def detect_from_song(self, song_object):
        with self._music_db.open() as odb:
            if not odb.does_song_match(song_object):
                print "Song could not be deteced (does not match db format)."
                return

        test_data = None
        try:
            test_data = self._feature_extractor.extract(song_object)
        except Exception as e:
            print "Error in extracting features from song: {}".format(e.message)
            return

        try:
            pred = self._regressioner.predict_proba(np.array([test_data]))
            return pred[0][0]
        except Exception as e:
            pass

        try:
            pred = self._regressioner.predict(np.array([test_data]))
            return pred[0]
        except Exception as e:
            print "Error in predicting song: {}".format(e.message)

    def detect_from_file(self, song_file_path, file_format):
        test_song = None
        if file_format == "mp3":
            test_song = pydub.AudioSegment.from_mp3(song_file_path)
        elif file_format == "wav":
            test_song = pydub.AudioSegment.from_wav(song_file_path)
        else:
            raise Exception("File format not supported.")

        return self.detect_from_song(test_song)


def main():
    if len(sys.argv) != 4:
        print "Bad usage! usage is {} " \
              "<music-db-folder> <test-path> <test-format>".format(sys.argv[0])
        return

    music_db_folder = sys.argv[1]
    test_path = sys.argv[2]
    test_format = sys.argv[3]

    clf = sklearn.svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)  # Todo: switch back?
    # clf = svm.SVC()
    # clf = lsanomaly.LSAnomaly()
    detector = MusicDetector(music_db_folder, clf)
    pred = detector.detect_from_file(test_path, test_format)
    print "pred for {} is {}".format(test_path, pred)


if __name__ == "__main__":
    main()
