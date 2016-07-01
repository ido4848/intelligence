import intelligent_creation

'''
functions should contain
def path_to_item(path)
def item_to_features(item)
def genome_to_item(genome)
def save_item(item, save_path)
def get_item_genome()
'''


def get_mp3_functions():
    functions = {}

    def path_to_item(path):
        pass

    def item_to_features(item):
        pass

    def genome_to_item(genome):
        pass

    def save_item(item, save_path):
        pass

    def get_item_genome():
        pass

    functions['path_to_item'] = path_to_item
    functions['item_to_features'] = item_to_features
    functions['genome_to_item'] = genome_to_item
    functions['save_item'] = get_item_genome
    functions['get_item_genome'] = get_item_genome

    return functions


def mp3_main():
    positive_folder = ""
    iterations = 10
    freq_stats = 5
    item_path = ""
    detector_path = ""
    functions = get_mp3_functions()
    verbose = True
    setup = True

    intelligent_creation.main_logic(functions, positive_folder, iterations, freq_stats, item_path,
                                    detector_path=detector_path, setup=setup, verbose=verbose)


def get_midi_functions():
    functions = {}

    def path_to_item(path):
        pass

    def item_to_features(item):
        pass

    def genome_to_item(genome):
        pass

    def save_item(item, save_path):
        pass

    def get_item_genome():
        pass

    functions['path_to_item'] = path_to_item
    functions['item_to_features'] = item_to_features
    functions['genome_to_item'] = genome_to_item
    functions['save_item'] = get_item_genome
    functions['get_item_genome'] = get_item_genome

    return functions


def midi_main():
    positive_folder = ""
    iterations = 10
    freq_stats = 5
    item_path = ""
    detector_path = ""
    functions = get_midi_functions()
    verbose = True
    setup = True

    intelligent_creation.main_logic(functions, positive_folder, iterations, freq_stats, item_path,
                                    detector_path=detector_path, setup=setup, verbose=verbose)


def main():
    mp3_main()


if __name__ == "__main__":
    main()
