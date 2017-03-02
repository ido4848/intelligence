from pyevolve import GSimpleGA
from pyevolve import Selectors


class Creator(object):
    def __init__(self, detector, get_genome, genome_to_item, verbose=True):
        self._detector = detector
        self._get_genome = get_genome
        self._genome_to_item = genome_to_item

        self._verbose = verbose

    def create(self, iterations, freq_stats=0):
        def eval_func(raw_genome):
            item = self._genome_to_item(raw_genome)
            pred = self._detector.detect(item)
            return pred

        # Enable the pyevolve logging system
        # pyevolve.logEnable("/dev/null")

        genome = self._get_genome()
        # The evaluator function (evaluation function)
        genome.evaluator.set(eval_func)

        # Genetic Algorithm Instance
        ga = GSimpleGA.GSimpleGA(genome)

        # Set the Roulette Wheel selector method, the number of generations and
        # the termination criteria
        ga.selector.set(Selectors.GRouletteWheel)
        ga.setGenerations(iterations)
        #ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)

        # Sets the DB Adapter, the resetDB flag will make the Adapter recreate
        # the database and erase all data every run, you should use this flag
        # just in the first time, after the pyevolve.db was created, you can
        # omit it.
        # sqlite_adapter = DBAdapters.DBSQLite(identify="ex1", resetDB=True)
        # ga.setDBAdapter(sqlite_adapter)

        # Do the evolution, with stats dump
        # frequency of 20 generations
        ga.evolve(freq_stats=freq_stats)

        # Best individual
        best = ga.bestIndividual()
        return best
