# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import pytest
from biosim.landscapes import Landscape
from biosim.animals import Animals, Herbivore, Carnivore


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
    assert l_scape.herbivore_list == l_scape.animals_die()
