# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

import pytest
from biosim.animals import Herbivore, Carnivore
from biosim.landscapes import Landscape
import biosim.island
import random


def test_init():
    """
    Test that the init method works for both carnivores and herbivores.
    """
    carn = Carnivore(3, 40)
    herb = Herbivore(2, 27)

    assert carn.weight == 40
    assert carn.age == 3

    assert herb.weight == 27
    assert herb.age == 2


def test_ageing():
    """
    Test that the animals ages the right way
    """
    herbivore = Herbivore(10, 20)
    assert herbivore.age == 10

    herbivore.aging()
    assert herbivore.age == 11


def test_weight_loss():
    """
    Test that the animals loses weight for every year
    """
    herbivore = Herbivore(9, 30)
    herbivore.weight_loss()

    assert not herbivore.weight == 30
    assert herbivore.weight == 28.5


def test_weight_gain():
    """
    Test that the animals gains the right amount of weight after eating"
    """
    cell = Landscape()
    initial_pop = [{'species': 'Herbivore', 'age': 1, 'weight': 20}]
    cell.set_population(initial_pop)
    cell.f_max = 800
    cell.food_grows()
    cell.animals_eat()

    assert cell.animal_list[0].weight != 20
    assert cell.animal_list[0].weight == 29


def test_fitness():
    """
    Testing that the fitness function works, that the fitness chances when animal aging
    """
    herbivore = Herbivore(5, 10)
    fitness_before = herbivore.fitness

    herbivore.aging()

    fitness_after = herbivore.fitness

    assert fitness_before != fitness_after


def test_death():
    """
    Testing that the animal dies if the weight is zero
    """

    herbivore = Herbivore(3, 0)

    assert herbivore.death() is True


def test_birth():
    """
    Test that the animals can't reproduce if only one animal is present"
    """
    cell = Landscape()

    initial_pop = [{'species': 'Herbivore', 'age': 1, 'weight': 10.}]

    cell.set_population(initial_pop)

    assert cell.animals_reproduce() is False
