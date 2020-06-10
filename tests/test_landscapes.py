# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import pytest
from biosim.landscapes import Landscape
from biosim.animals import Animals, Herbivore, Carnivore
import random

random.seed(12345)


@pytest.fixture()
def initial_populations():
    init_pop = [{"species": "Herbivore", "age": 1, "weight": 10.0},
                {"species": "Carnivore", "age": 3, "weight": 14.0}]
    return init_pop


def test_set_population(initial_populations):
    l_scape = Landscape()
    l_scape.set_population(initial_populations)
    assert type(l_scape.herbivore_list[0]) == Herbivore
    assert type(l_scape.carnivore_list[0]) == Carnivore


def test_food_grows():
    l_scape = Landscape()
    l_scape.available_food = 0
    l_scape.f_max = 800
    l_scape.food_grows()

    assert l_scape.available_food != 0
    assert l_scape.available_food == 800


def test_animal_eats():
    l_scape = Landscape()


def test_reproduce_herbivore():
    init_pop = [{"species": "Herbivore", "age": 3, "weight": 50.0},
                {"species": "Herbivore", "age": 3, "weight": 54.0},
                {"species": "Herbivore", "age": 3, "weight": 50.0},
                {"species": "Herbivore", "age": 3, "weight": 54.0}]

    l_scape = Landscape()
    l_scape.set_population(init_pop)

    l_scape.herbivore_reproduce()

    assert len(l_scape.herbivore_list) != 4


def test_reproduce_carnivore():
    init_pop = [{"species": "Carnivore", "age": 3, "weight": 50.0},
                {"species": "Carnivore", "age": 3, "weight": 54.0},
                {"species": "Carnivore", "age": 3, "weight": 50.0},
                {"species": "Carnivore", "age": 3, "weight": 54.0}]

    l_scape = Landscape()
    l_scape.set_population(init_pop)

    l_scape.carnivore_reproduce()

    assert len(l_scape.carnivore_list) != 4


def test_animals_die(initial_populations):
    l_scape = Landscape()
    l_scape.set_population(initial_populations)

    old_pop = (l_scape.carnivore_list + l_scape.herbivore_list)
    l_scape.animals_die()

    new_pop = (l_scape.carnivore_list + l_scape.herbivore_list)

    assert old_pop != new_pop


def test_animals_age(initial_populations):
    l_scape = Landscape()
    l_scape.set_population(initial_populations)

    l_scape.animals_age()

    new_herbivore = l_scape.herbivore_list[0].age
    new_carnivore = l_scape.carnivore_list[0].age

    assert 2 == new_herbivore
    assert 4 == new_carnivore


def test_animals_weight_loss(initial_populations):
    l_scape = Landscape()
    l_scape.set_population(initial_populations)

    l_scape.animals_lose_weight()

    new_herbivore_weight = l_scape.herbivore_list[0].weight
    new_carnivore_weight = l_scape.carnivore_list[0].weight

    assert new_carnivore_weight == 12.25
    assert new_herbivore_weight == 9.5
