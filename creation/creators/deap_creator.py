import random

import numpy
from deap import base, creator, tools, algorithms

from utilization.value_lists import ValueList


class DeapCreator(object):
    def __init__(self, trained_regressor, value_list_to_item, config, verbose=True):
        self._trained_regressor = trained_regressor
        self._value_list_to_item = value_list_to_item

        self._config = config
        self._verbose = verbose

    def _create(self):
        def eval_func(genome_list):
            value_list = ValueList(genome_list)
            item = self._value_list_to_item(value_list)
            pred = self._trained_regressor.predict_proba(item)
            return pred,

        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax)

        toolbox = base.Toolbox()

        toolbox.register("attr_float", random.random)
        toolbox.register("individual", tools.initRepeat, creator.Individual,
                         toolbox.attr_float, self._config['genome_size'])

        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", eval_func)
        toolbox.register("mate", tools.cxBlend, alpha=0.1)
        toolbox.register("mutate", tools.mutGaussian, mu=0.5, sigma=0.5, indpb=0.05)
        toolbox.register("select", tools.selBest)

        pop = toolbox.population(n=self._config['population_size'])
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", numpy.mean)
        stats.register("std", numpy.std)
        stats.register("min", numpy.min)
        stats.register("max", numpy.max)

        pop, log = algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=self._config['num_of_generations'],
                                       stats=stats, halloffame=hof, verbose=self._verbose)
        return pop

    def create(self):
        return self._create()[0]

    def create_many(self, n):
        many = self._create()
        while len(many) < n:
            many += self._create()
        return many[0:n]
