# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import pytest
from biosim.animals import Animals, Herbivore, Carnivore
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
    Test that the both herbivore and carnivore ages the right way
    """
    herbivore = Herbivore(10, 20)
    carnivore = Carnivore(10, 20)
    assert herbivore.age == 10
    assert carnivore.age == 10

    herbivore.aging()
    carnivore.aging()
    assert herbivore.age == 11
    assert carnivore.age == 11


def test_weight_loss():
    """
    Test that the animals loses weight for every year
    """
    herbivore = Herbivore(9, 30)
    herbivore.weight_loss()

    carnivore = Carnivore(9, 40)
    carnivore.weight_loss()

    assert herbivore.weight != 30
    assert herbivore.weight == 28.5

    assert carnivore.weight != 40
    assert carnivore.weight == 35


def test_weight_gain_eating_herbivore():
    """
    Test that the animals gains the right amount of weight after eating"
    """

    herbivore = Herbivore(5, 10)

    herbivore.eats(10)

    assert herbivore.weight != 10
    assert herbivore.weight == 19


def test_weight_gain_eating_carnivore():
    carnivore = Carnivore(5, 10)
    herbivore = Herbivore(6, 20)

    carnivore.eat(herbivore)

    assert carnivore.weight != 20
    assert carnivore.weight == 25


def test_fitness_aging():
    """
    Testing that the fitness function works, that the fitness changes when animal aging
    """
    herbivore = Herbivore(5, 10)
    fitness_before_herbivore = herbivore.fitness

    carnivore = Carnivore(5, 30)
    fitness_before_carnivore = carnivore.fitness

    herbivore.aging()
    carnivore.aging()

    fitness_after_herbivore = herbivore.fitness
    fitness_after_carnivore = carnivore.fitness

    assert fitness_before_herbivore != fitness_after_herbivore
    assert fitness_before_carnivore != fitness_after_carnivore


def test_fitness_function():
    """
    Testing if the fitness is calculated the right way
    """
    herbivore = Herbivore(5, 10)
    carnivore = Carnivore(5, 20)

    assert herbivore.fitness == 0.49999999962087194
    assert carnivore.fitness == 0.998313708904945


def test_death_weight():
    """
    Testing that the animal dies if the weight is zero
    """

    herbivore = Herbivore(3, 0)
    carnivore = Carnivore(5, 0)

    assert herbivore.death() is True
    assert carnivore.death() is True


def test_death_probability():
    herbivore = Herbivore(5, 10)
    carnivore = Carnivore(6, 15)
    list_ = []
    for _ in range(100):
        list_.append(herbivore.death())
        list_.append(carnivore.death())
    assert True in list_
    assert False in list_


def test_birth():
    """
    Test that the animals can't reproduce if only one animal is present"
    """
    cell = Landscape()

    initial_pop = [{"species": "Herbivore", "age": 1, "weight": 10.0},
                   {"species": "Carnivore", "age": 1, "weight": 10.0}, ]

    cell.set_population(initial_pop)

    assert cell.herbivore_reproduce() is False
    assert cell.carnivore_reproduce() is False
