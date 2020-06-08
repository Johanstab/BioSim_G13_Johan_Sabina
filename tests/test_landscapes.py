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
    assert type(l_scape.animal_list[0]) == Herbivore
    assert type(l_scape.animal_list[1]) == Carnivore


def test_food_grows():
    pass


def test_animal_eats():
    pass


def test_animals_reproduce():
    pass


def test_animals_die():
    pass
