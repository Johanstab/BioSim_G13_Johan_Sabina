# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import pytest
from biosim.animals import Animals, Herbivore, Carnivore


def test_set_params():
    params = Herbivore.params
    new_params = {
        "w_birth": 12.0,
        "sigma_birth": 1.2,
        "beta": 0.8,
        "eta": 0.01,
        "a_half": 35.0,
        "phi_age": 0.4,
        "w_half": 14.0,
        "phi_weight": 0.2,
        "mu": 0.50,
        "gamma": 0.3,
        "zeta": 3.75,
        "xi": 1.552,
        "omega": 0.41,
        "F": 12.0,
    }
    new_params = Herbivore.set_params(new_params)
    assert new_params != params


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


def test_age():
    """
    Test that it is possible to set and get the age of animals.
    """
    herbivore = Herbivore(10, 20)
    carnivore = Carnivore(10, 20)
    assert herbivore.age == 10
    assert carnivore.age == 10

    herbivore.age = 12
    carnivore.age = 12
    assert herbivore.age == 12
    assert carnivore.age == 12


def test_ageing():
    """
    Test that the both herbivore and carnivore ages the right way.
    """
    herbivore = Herbivore(10, 20)
    carnivore = Carnivore(10, 20)

    herbivore.aging()
    carnivore.aging()
    assert herbivore.age == 11
    assert carnivore.age == 11


def test_weight():
    """
    Tests that it is possible to set and get weight of an animal.
    """
    herbivore = Herbivore(10, 20)
    carnivore = Carnivore(10, 20)

    assert herbivore.weight == 20
    assert carnivore.weight == 20

    herbivore.weight = 30
    carnivore.weight = 30
    assert herbivore.weight == 30
    assert carnivore.weight == 30


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


def test_weight_gain_eating_carnivore(mocker):
    mocker.patch('numpy.random.random', return_value=0.0000001)
    carnivore = Carnivore(5, 20)
    herbivore = [Herbivore(6, 20)]
    herbivore = carnivore.eat(herbivore)
    assert carnivore.weight != 20
    assert carnivore.weight == 35

    assert herbivore == []


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


def test_fitness_weight_loss():
    herbivore = Herbivore(5, 10)
    fitness_before_herbivore = herbivore.fitness

    carnivore = Carnivore(5, 30)
    fitness_before_carnivore = carnivore.fitness

    herbivore.weight_loss()
    carnivore.weight_loss()

    fitness_after_herbivore = herbivore.fitness
    fitness_after_carnivore = carnivore.fitness

    assert fitness_before_herbivore != fitness_after_herbivore
    assert fitness_before_carnivore != fitness_after_carnivore


def test_fitness_weight_zero():
    herbivore = Herbivore(5, 0)
    carnivore = Carnivore(5, 0)
    assert herbivore.fitness == 0
    assert carnivore.fitness == 0


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


def test_death_probability(mocker):
    mocker.patch('numpy.random.random', return_value=0.000001)
    herbivore = Herbivore(5, 10)
    carnivore = Carnivore(6, 15)
    assert herbivore.death() is True
    assert carnivore.death() is True


def test_birth(mocker):
    """
    Test that the animals can't reproduce if only one animal is present"
    """
    mocker.patch('numpy.random.random', return_value=0.000001)
    herbivore = Herbivore(5, 35)
    carnivore = Carnivore(5, 30)
    nr_animals = 10

    assert herbivore.birth(nr_animals) is not None
    assert carnivore.birth(nr_animals) is not None


def test_no_birth_baby_to_heavy(mocker):
    mocker.patch('numpy.random.normal', return_value=50)
    mocker.patch('numpy.random.random', return_value=0.00001)
    herbivore = Herbivore(5, 35)
    carnivore = Carnivore(5, 30)
    nr_animals = 10

    assert herbivore.birth(nr_animals) is None
    assert carnivore.birth(nr_animals) is None


def test_loose_weight_when_birth(mocker):
    mocker.patch('numpy.random.normal', return_value=20)
    mocker.patch('numpy.random.random', return_value=0.00001)
    herbivore = Herbivore(5, 35)
    carnivore = Carnivore(5, 30)
    nr_animals = 10

    herbivore.birth(nr_animals)
    carnivore.birth(nr_animals)

    assert herbivore.weight == 11
    assert carnivore.weight == 8


def test_move(mocker):
    mocker.patch('numpy.random.random', return_value=0.0000001)
    herbivore = Herbivore(5, 20)
    carnivore = Carnivore(5, 20)
    assert herbivore.move() is True
    assert carnivore.move() is True

