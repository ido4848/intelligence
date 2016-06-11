import sys
import os
import crawl_music_folder
import detect_mp3


def detect_all(db_folder, test_folder):
    for root, _, file_names in os.walk(test_folder):
        for file_name in file_names:
            detect_mp3.detect_mp3(db_folder, root + "/" + file_name)

def main():
    if len(sys.argv) != 4:
        print "Bad usage! usage is {} " \
            "<train_music_folder>" \
            " <music-db-folder> <test_music_folder>".format(sys.argv[0])
        return

    train_folder = sys.argv[1]
    db_folder = sys.argv[2]
    test_folder = sys.argv[3]


    crawl_music_folder.crawl_music_folder(train_folder, db_folder)
    detect_all(db_folder, test_folder)


if __name__ == "__main__":
    main()
