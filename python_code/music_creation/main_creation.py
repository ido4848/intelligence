import array, random
from deap import creator, base, tools, algorithms

from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Statistics
from pyevolve import DBAdapters
import pyevolve
from pyevolve import Initializators, Mutators

def pyevolve_continues_example():
    # Find negative values
    def eval_func(ind):
       score = 0.0
       for x in xrange(0,len(ind)):
          if ind[x] <= 0.0: score += 0.1
       return score

    # Genome instance
    genome = G1DList.G1DList(20)
    genome.setParams(rangemin=-6.0, rangemax=6.0)

    # Change the initializator to Real values
    genome.initializator.set(Initializators.G1DListInitializatorReal)

    # Change the mutator to Gaussian Mutator
    genome.mutator.set(Mutators.G1DListMutatorRealGaussian)

    # The evaluator function (objective function)
    genome.evaluator.set(eval_func)

    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)
    ga.selector.set(Selectors.GRouletteWheel)
    ga.nGenerations = 100

    # Do the evolution
    ga.evolve()

    # Best individual
    best = ga.bestIndividual()
    print best.genomeList


def pyevolve_discrete_example():
    # This function is the evaluation function, we want
    # to give high score to more zero'ed chromosomes
    def eval_func(chromosome):
        score = 0.0

        # iterate over the chromosome
        # score = len(filter(lambda x: x==0, chromosome.genomeList))
        for value in chromosome:
            if value == 0:
                score += 1

        return score

    # Enable the pyevolve logging system
    # pyevolve.logEnable("/dev/null")

    # Genome instance, 1D List of 50 elements
    genome = G1DList.G1DList(50)

    # Sets the range max and min of the 1D List
    genome.setParams(rangemin=0, rangemax=255)

    # The evaluator function (evaluation function)
    genome.evaluator.set(eval_func)

    # Genetic Algorithm Instance
    ga = GSimpleGA.GSimpleGA(genome)

    # Set the Roulette Wheel selector method, the number of generations and
    # the termination criteria
    ga.selector.set(Selectors.GRouletteWheel)
    ga.setGenerations(500)
    ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)

    # Sets the DB Adapter, the resetDB flag will make the Adapter recreate
    # the database and erase all data every run, you should use this flag
    # just in the first time, after the pyevolve.db was created, you can
    # omit it.
    # sqlite_adapter = DBAdapters.DBSQLite(identify="ex1", resetDB=True)
    # ga.setDBAdapter(sqlite_adapter)

    # Do the evolution, with stats dump
    # frequency of 20 generations
    ga.evolve()

    # Best individual
    best = ga.bestIndividual()
    print best.genomeList

def deap_example():
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", array.array, typecode='b', fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.randint, 0, 1)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool , 2)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    def evalOneMax(individual):
        return sum(individual),

    toolbox.register("evaluate", evalOneMax)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    population = toolbox.population(n=100)

    NGEN = 40
    for gen in range(NGEN):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        population = offspring

    print population


def main():
    # pyevolve_continues_example()
    pyevolve_discrete_example()
    # deap_example()

if __name__ == "__main__":
    main()
