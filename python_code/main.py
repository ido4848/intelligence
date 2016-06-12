import sys
import folder_crawler
import music_detector
import featured_music_db
import feature_extractors

from lsanomaly import LSAnomaly
from sklearn import svm
from sklearn import linear_model
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR


def detect_all(detector, test_folder):
    mp3_song_files = folder_crawler.collect_file_paths(test_folder, "[Mm][Pp]3")
    wav_song_files = folder_crawler.collect_file_paths(test_folder, "[Ww][Aa][Ww]")

    for mp3_song in mp3_song_files:
        pred = detector.detect(mp3_song, "mp3")
        print "prediction for {} is {} ({})".format(mp3_song, pred, pred >= 0.5)
        print

    for wav_song in wav_song_files:
        pred = detector.detect(wav_song, "wav")
        print "prediction for {} is {} ({})".format(wav_song, pred, pred >= 0.5)
        print


FRAME_RATE = 44100
CHANNELS = 2


def unit_print(msg):
    print "********************************** " + msg + " **********************************"


def main_logic(train_folder, db_folder, test_folder, setup=True):
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

    ''' DETECTING '''
    detect_all(detector, test_folder)
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
    setup = raw_input("setup(1/0): ")
    main_logic("/home/ido4848/Music/mp3s/train", "/home/ido4848/DB/raw_songs", "/home/ido4848/Music/mp3s",
               setup=bool(setup))

'''
REFACTORING:
    TODOS
    SONGS, METADATA IN THE SAME DB?
'''

'''
IMPROVMENTS:
    DB_SIZE
    FEATURE_EXTRACTION
    ALGORITHM
'''
