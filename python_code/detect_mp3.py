# -*- coding: utf-8 -*-
from sklearn import svm
import numpy as np
import pickle
import sys
import pydub
from sklearn.externals import joblib


def restore_detector(clf_name):
    return joblib.load(clf_name + "/clffile.pkl")


def main():
    if len(sys.argv) != 3:
        print "Bad usage! usage is {} " \
            "<classifier-name> <mp3-sample-path>".format(sys.argv[0])
        return

    clf_name = sys.argv[1]
    sample_path = sys.argv[2]

    clf = restore_detector(clf_name)

    sample = pydub.AudioSegment.from_mp3(sample_path)
    print sample.frame_rate
    sample_cut = sample[0:10000:]
    sample_cut_array = list(sample_cut.raw_data)
    sample_cut_test = [ord(c) for c in sample_cut_array]

    pred = clf.predict(np.array([sample_cut_test]))

    if pred[0] == 1:
        print "Sample {} is music!".format(sample_path)
    else:
        print "Sample {} is not music!".format(sample_path)

if __name__ == "__main__":
    main()
