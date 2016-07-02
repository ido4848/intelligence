import crawling
import creation
import detection
import saving


def main_logic(functions, positive_folder, iterations, freq_stats, item_path,
               detector_path=None, setup=True, verbose=True):
    detector = None
    if setup:
        positive_set = crawling.FolderCrawler.crawl(positive_folder, functions['path_to_item'])
        if verbose:
            print "**************** positive set was crawled ****************"
        detector = detection.Detector(positive_set, None, functions['item_to_features'])
        if verbose:
            print "**************** detector was trained ****************"
        if detector_path is not None:
            saving.Saver.save(detector, detector_path)
            if verbose:
                print "**************** detector was saved ****************"
    elif detector_path is not None:
        detector = saving.load(detector_path)
        if verbose:
            print "**************** detector was loaded from file ****************"
    else:
        print "Could not get detector, as setup is False and there is no saved detector."
        return

    creator = creation.Creator(detector, functions['get_item_genome'], functions['genome_to_item'])
    if verbose:
        print "**************** creator was created ****************"
    best_item = functions['genome_to_item'](creator.create(iterations, freq_stats))
    if verbose:
        print "**************** best item was created ****************"
    functions['save_item'](best_item, item_path)
    if verbose:
        print "**************** best item was saved correctly ****************"
