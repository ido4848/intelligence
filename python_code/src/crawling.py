import os


class FolderCrawler(object):
    @staticmethod
    def crawl(folder, path_to_item, verbose=True):
        items = []
        for root, _, file_names in os.walk(folder):
            for file_name in file_names:
                full_path = root + "/" + file_name
                try:
                    items.append(path_to_item(full_path))
                except Exception as e:
                    if verbose:
                        print "Could not create item from path {} : {}".format(full_path, e.message)

        if verbose:
            print "{} items were crawled".format(len(items))
        return items
