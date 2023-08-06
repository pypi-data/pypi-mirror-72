# ======================================================================
# pynetics: a simple yet powerful evolutionary computation library
# Copyright (C) 2020 Alberto Díaz-Álvarez
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# “Software”), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH
# THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ======================================================================
"""Implementation of different Evolutionary Computation algorithms.

Currently only one implementation (Genetic Algorithm) is provided.
"""
from __future__ import annotations

import inspect
import math
import random
from collections import Sequence
from typing import Tuple, Optional

from . import api, callback
from .exception import NotInitialized
from .util import take_chances


class GeneticAlgorithm(api.EvolutiveAlgorithm):
    """Modular implementation of a canonical genetic algorithm.

    Each step the algorithm will generate a new offspring population
    from the previous one, and then invoke the replacement schema to
    combine the old and new genotypes in a new population ready to use
    in a new algorithm step.

    The step consists in a loop where the selection, replacement and
    mutation operators take part. This loop will end when the offspring
    population is filled.
    """

    def __init__(
            self, *,
            population_size: int,
            initializer: api.Initializer,
            stop_condition: api.StopCondition,
            fitness: api.Fitness,
            selection: api.Selection,
            replacement: Tuple[api.Replacement, float],
            recombination: api.Recombination = None,
            recombination_probability: float = None,
            mutation: Optional[api.Mutation] = None,
            mutation_probability: Optional[float] = None,
            callbacks: Sequence[callback.Callback] = None,
    ):
        """Initializes this object

        :param population_size: The population size. Must be greater
            than zero.
        :param initializer: TODO TBD
        :param stop_condition: When does the algorithm stop.
        :param fitness: TODO TBD
        :param selection: The algorithm that selects one phenotype
            from the population.
        :param recombination: The recombination schema to apply to the
            selected genotypes.
        :param recombination_probability: The probability for some
            genotypes to be recombined. It must be a numeric value (or a
            string with a float value in it) belonging to the [0, 1]
            interval. Any value out of that interval will be truncated.
        :param mutation: The mutation schema to apply to the genotypes.
        :param mutation_probability: The probability for a genotype to
            mutate. It must be a numeric value (or a string with a float
            value in it) belonging to the [0, 1] interval. Any value out
            of that interval will be truncated.
        :param replacement: A tuple with the replacement algorithm as
            the first element, and the replacement rate for a phenotypes
            to mutate. The probability must be a float value belonging
            to the [0, 1] interval.
        :param callbacks: TODO TBD...
        """
        super().__init__(stop_condition=stop_condition, callbacks=callbacks)

        self.population_size = population_size
        self.initializer = initializer
        self.stop_condition = stop_condition
        self.fitness = fitness
        self.selection = selection

        # The recombination is optional, so in case no recombination is
        # provided, the mutation operation will be the identity (that
        # is, return the same, unmodified, genotypes.
        self.recombination = recombination
        self.recombination_probability = recombination_probability

        # The mutation is optional, so in case no mutation is provided,
        # the mutation operation will be the identity (that is, return
        # the same, unmodified, genotype.
        self.mutation = mutation
        self.mutation_probability = mutation_probability

        self.replacement, self.replacement_rate = replacement
        # The offspring size is based on the original population size
        # and the replacement rate
        self.offspring_size = math.ceil(
            self.population_size * self.replacement_rate
        )

        # Dynamic selection size computation based on the number of
        # arguments required by the recombination method
        self.selection_size = len(
            inspect.signature(self.recombination).parameters
        )

        # The population held in this algorithm. This variable will
        # always contain the population corresponding to the current
        # generation.
        self.population = api.Population(self.population_size, self.fitness)

    @property
    def recombination(self) -> api.Recombination:
        """TODO TBD"""
        return self.__recombination

    @recombination.setter
    def recombination(self, recombination: api.Recombination):
        """TODO TBD"""
        self.__recombination = recombination or (lambda *g: g)

    @property
    def recombination_probability(self) -> float:
        """TODO TBD"""
        return self.__recombination_probability

    @recombination_probability.setter
    def recombination_probability(self, probability: float):
        """TODO TBD"""
        if probability is None:
            probability = 0
        self.__recombination_probability = max(min(float(probability), 1), 0)

    @property
    def mutation(self) -> api.Mutation:
        """TODO TBD"""
        return self.__mutation

    @mutation.setter
    def mutation(self, mutation: api.Mutation):
        """TODO TBD"""
        self.__mutation = mutation or (lambda _, g: g)

    @property
    def mutation_probability(self) -> float:
        """TODO TBD"""
        return self.__mutation_probability

    @mutation_probability.setter
    def mutation_probability(self, probability: float):
        """TODO TBD"""
        if probability is None:
            probability = 0
        self.__mutation_probability = max(min(float(probability), 1), 0)

    def on_initialize(self):
        # Renew the population
        self.population.clear()
        self.initializer.fill(self.population)

    def on_finalize(self):
        pass

    def step(self):
        """The particular implementation of this genetic algorithm.

        The inner working is as follows:
        """
        # Create the new empty population to hold the new offspring.
        offspring = api.Population(
            size=self.offspring_size,
            fitness=self.fitness
        )

        # Fill the offspring with the genotypes following the standard
        # genetic algorithm schema
        while not offspring.full():
            # Select the required number of genotypes according to the
            # needed by the crossover algorithm
            selected = self.selection(self.population, self.selection_size)

            # Recombine the selected genotypes to get the new progeny
            if take_chances(self.recombination_probability):
                selected = self.recombination(*selected)

            # Adjust the progeny size to avoid the problem of ending
            # with a new population of different size
            size = min(len(selected), offspring.max_size - len(offspring))
            selected = (g for g in random.sample(selected, size))

            # Mutate the genotypes if there is a chance
            mutated_progeny = (
                self.mutation(self.mutation_probability, g)
                for g in selected
            )

            # Add progeny to the offspring
            offspring.extend(mutated_progeny)

        # Replacement
        self.population = self.replacement(
            population=self.population,
            offspring=offspring,
        )

    def best(self) -> api.Genotype:
        """The best genotype obtained so far.

        :return: The best genotype obtained at the moment of calling.
        :raise: NotInitialized if the population hasn't be created yet.
        """
        if self.population.empty():
            raise NotInitialized()
        else:
            self.population.sort()
            return self.population[-1]
