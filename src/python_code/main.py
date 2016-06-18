import sys

import feature_extractors
import featured_music_db
import folder_crawler
import music_detector

import imp

LSAnomaly = imp.load_source("LSAnomaly", r'../../modules/lsanomaly/lsanomaly.py')


def detect_weighted(detector, test_folder, weight):
    mp3_song_files = folder_crawler.collect_file_paths(test_folder, "[Mm][Pp]3")
    wav_song_files = folder_crawler.collect_file_paths(test_folder, "[Ww][Aa][Ww]")

    total_count = len(mp3_song_files) + len(wav_song_files)
    success_count = 0

    pred_sum = 0

    predictions = {}
    for mp3_song in mp3_song_files:
        predictions[mp3_song] = detector.detect_from_file(mp3_song, "mp3")
    for wav_song in wav_song_files:
        predictions[wav_song] = detector.detect_from_file(wav_song, "wav")

    for song, pred in predictions.iteritems():
        if pred is None:
            total_count -= 1
            continue
        pred_sum += pred
        if weight > 0:
            if pred >= weight:
                success_count += 1
            else:
                print "(failed) prediction for {} is {}".format(song, pred)
        else:
            if pred <= -weight:
                success_count += 1
            else:
                print "(failed) prediction for {} is {}".format(song, pred)

    print "{} out of {} detected successfully, for weight {} in folder {}".format(success_count, total_count,
                                                                                  weight, test_folder)
    print "Average is {}".format(pred_sum / float(total_count))


def detect_neutral(detector, test_folder):
    mp3_song_files = folder_crawler.collect_file_paths(test_folder, "[Mm][Pp]3")
    wav_song_files = folder_crawler.collect_file_paths(test_folder, "[Ww][Aa][Ww]")

    for mp3_song in mp3_song_files:
        pred = detector.detect_from_file(mp3_song, "mp3")
        print "prediction for {} is {} ({})".format(mp3_song, pred, pred >= 0.5)
        print

    for wav_song in wav_song_files:
        pred = detector.detect_from_file(wav_song, "wav")
        print "prediction for {} is {} ({})".format(wav_song, pred, pred >= 0.5)
        print


def detect_all(detector, test_folders):
    for folder_type, test_folder in test_folders:
        if folder_type == 0:
            detect_neutral(detector, test_folder)
        else:
            detect_weighted(detector, test_folder, folder_type)
        print


FRAME_RATE = 44100
CHANNELS = 2


def unit_print(msg):
    print "********************************** " + msg + " **********************************"


def get_detector(train_folder, db_folder, setup=True):
    ''''''

    if setup:
        ''' CRAWLING '''
        crawler = folder_crawler.fileExtensionFolderCrawler(train_folder)
        mp3_song_files = crawler.crawl_by_extension("[Mm][Pp]3")
        wav_song_files = crawler.crawl_by_extension("[Ww][Aa][Ww]")
        unit_print("{} songs were discoverd during crawling.".format(len(mp3_song_files) + len(wav_song_files)))

        ''' DB BUILDING '''
        # extractor = feature_extractors.RawDataFeatureExtractor()
        extractor = feature_extractors.ChristianPecceiFeatureExtractor()

        db = featured_music_db.FeaturedMusicDB.create_new(db_folder, FRAME_RATE, CHANNELS, extractor)
        with db.open() as odb:
            odb.add_mp3s(mp3_song_files)
            odb.add_wavs(wav_song_files)
        unit_print("DB was built.")

    ''' TRAINING '''
    # clf = svm.SVC()
    clf = LSAnomaly()
    # clf = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)  # Todo: switch back?
    # clf = linear_model.ElasticNet()
    # clf = DecisionTreeRegressor(max_depth=5)
    # clf = SVR(kernel='rbf', C=1e3, gamma=0.1)
    detector = music_detector.MusicDetector(db_folder, clf)
    unit_print("Detector was trained")
    return detector


def main_logic(train_folder, db_folder, test_folders, setup=True):
    ''''''
    detector = get_detector(train_folder, db_folder, setup)
    ''' DETECTING '''
    detect_all(detector, test_folders)
    unit_print("Songs were deteceted")


def main():
    if len(sys.argv) != 4:
        print "Bad usage! usage is {} " \
              "<train_music_folder>" \
              " <music-db-folder> <test_music_folder>".format(sys.argv[0])
        return
    main_logic(sys.argv[1], sys.argv[2], sys.argv[3])


if __name__ == "__main__":
    # main()
    setup = False
    if raw_input("setup(True/False): ") in ['true', 'True', "TRUE", 't', 'y', 'yes', 'Y', '1']:
        setup = True
    test_folders = [(0.5, "/home/ido4848/Music/mp3s/train"), (-0.5, "/home/ido4848/Music/mp3s/negative_test"),
                    (0.5, "/home/ido4848/Music/mp3s/positive_test")]
    main_logic("/home/ido4848/Music/mp3s/train", "/home/ido4848/DB/raw_songs", test_folders,
               setup=setup)

'''
REFACTORING:
    TODOS
    SONGS, METADATA IN THE SAME DB?
'''

'''
IMPROVMENTS:
    DB_SIZE (classical?)
    FEATURE_EXTRACTION (rosalib?)
    ALGORITHM (proba?, regression?)
'''
