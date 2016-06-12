# -*- coding: utf-8 -*-
import sys
import fnmatch
import os
from featured_music_db import FeaturedMusicDB
import feature_extractors


class fileExtensionFolderCrawler(object):
    def __init__(self, folder):
        self._folder = folder

    def crawl_by_extension(self, file_extension_regex):
        file_paths = []
        for root, _, file_names in os.walk(self._folder):
            for file_name in fnmatch.filter(file_names, '*.' + file_extension_regex):
                file_paths.append(root + "/" + file_name)
        return file_paths


def collect_file_paths(folder, file_extension_regex):
    file_paths = []
    for root, _, file_names in os.walk(folder):
        for file_name in fnmatch.filter(file_names, '*.' + file_extension_regex):
            file_paths.append(root + "/" + file_name)
    return file_paths


def main():
    pass


if __name__ == "__main__":
    main()
