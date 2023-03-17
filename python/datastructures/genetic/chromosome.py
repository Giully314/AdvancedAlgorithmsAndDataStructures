from dataclasses import dataclass
from typing import Callable
import random
from operator import itemgetter


@dataclass
class Individual:
    chromosome: list[int]

    def fitness(self):
        ...


@dataclass 
class CrossoverOperator:
    """ 
    Wrapper class for a crossover method.
    cross_method: function to apply for the crossover.
    chanche: probability to apply the crossover method.
    """ 
    cross_method: Callable[[Individual, Individual], Individual]
    chance: float

    def apply(self, p1: Individual, p2: Individual) -> Individual:
        if random.random() < self.chance:
            return self.cross_method(p1, p2)
        else:
            return random.choice([p1, p2]) 

@dataclass
class MutationOperator:
    """ 
    Wrapper class for a mutaton method.
    mutation_method: function to apply for the mutation (in place).
    chanche: probability to apply the mutation method.
    """ 
    mutation_method: Callable[[Individual], None] 
    chance: float
    mutation_chance: float = None # argument for the mutation_method

    def apply(self, x: Individual):
        if random.random() < self.chance:
            self.mutation_method(x, self.mutation_chance) 

def init_population(size: int, chromosome_init: Callable[[], list[int]]) -> list[Individual]:
    population: list[Individual] = []
    for _ in range(size):
        population.append(chromosome_init())
    return population



def natural_selection(population: list[Individual], elitism: Callable[[list[Individual]], list[Individual]],
                      select_for_mating: Callable[[list[Individual]], Individual],
                      crossover: CrossoverOperator, mutations: list[MutationOperator]) -> list[Individual]:
    """ 
    Main loop that simulate the creation of a new generation from an old one.
    """
    new_population = []
    if elitism is not None:
        new_population = elitism(population)
    while len(new_population) < len(population):
        individual_1 = select_for_mating(population)
        individual_2 = select_for_mating(population)
        new_individual = crossover.apply(individual_1, individual_2)
        for mutation in mutations:
            mutation.apply(new_individual)
        new_population.append(new_individual)
    return new_population



def tournament_selection(population: list[Individual], k: int):
    """ 
    This function select a mate for the creation of a new individual.
    k: number of random individuals to take from populations.
    return: the best from the k individual chosen. 
    Note that the probability to choose the individual with the lowest fitness is 1/len(population)^k.
    In general the probability to take the i-th highest individual is the same 1/len(population) * ((n-i)/n)^k.
    Note that we can also weight the probability to being chosen by the fitness of the individual (or the cumulative percentual
    like in the wheel selection but more expansive).
    """
    chosen_individuals = random.choices(population, k=k)
    fitnesses = [x.fitness for x in chosen_individuals]
    idx, value = max(enumerate(fitnesses), key=itemgetter(1))
    return chosen_individuals[idx] 