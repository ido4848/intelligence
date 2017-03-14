import numpy
import random

from deap import base, creator, tools, algorithms


class Creator(object):
    def __init__(self, detector, genome_to_item, verbose=True):
        self._detector = detector
        self._genome_to_item = genome_to_item

        self._verbose = verbose

    def create(self, params):
        def eval_func(raw_genome):
            item = self._genome_to_item(raw_genome)
            pred = self._detector.detect(item)
            return pred,

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()

        toolbox.register("attr_float", random.random)
        toolbox.register("individual", tools.initRepeat, creator.Individual,
                         toolbox.attr_float, params['genome_size'])

        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", eval_func)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)

        pop = toolbox.population(n=params['population_size'])
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=params['num_of_generations'],
                                       stats=stats, halloffame=hof, verbose=self._verbose)
        return pop
