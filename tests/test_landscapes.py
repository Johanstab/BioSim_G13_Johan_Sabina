# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import pytest
from biosim.landscapes import Landscape
from biosim.animals import Animals, Herbivore


def test_set_population():
    init_pop = {"species": "Herbivore", "age": 1, "weight": 10.0}
    l_scape = Landscape()
    set_pop = Landscape.set_population(l_scape, init_pop)
    assert l_scape.animal_list[0] == Herbivore


def test_food_grows():
    pass


def test_animal_eats():
    pass


def test_animals_reproduce():
    pass


def test_animals_die():
    pass
