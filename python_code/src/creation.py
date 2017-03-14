from pyevolve import GSimpleGA
from pyevolve import Selectors

from deap import base, creator, tools, algorithms
import numpy


class Creator(object):
    def __init__(self, detector, get_toolbox, genome_to_item, verbose=True):
        self._detector = detector
        self._toolbox = get_toolbox()
        self._genome_to_item = genome_to_item

        self._verbose = verbose

    def create(self, params):
        def eval_func(raw_genome):
            item = self._genome_to_item(raw_genome)
            pred = self._detector.detect(item)
            return pred,

        self._toolbox.register("evaluate", eval_func)
        self._toolbox.register("mate", tools.cxTwoPoint)
        self._toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        self._toolbox.register("select", tools.selTournament, tournsize=3)

        pop = self._toolbox.population(n=params['population_size'])
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        pop, log = algorithms.eaSimple(pop, self._toolbox, cxpb=0.5, mutpb=0.2, ngen=params['iterations'],
                                       stats=stats, halloffame=hof, verbose=self._verbose)
        return pop
