# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import pytest
from biosim.landscapes import Landscape, Lowland, Highland, Desert, Water
from biosim.animals import Herbivore, Carnivore


def test_set_params():
    params = Lowland.params
    new_params = {'f_max': 5000}
    new_params = Lowland.set_params(new_params)
    assert params != new_params


def test_set_params_error():
    new_params1 = {'fodder_max': 10}
    new_params2 = {'f_max': -10}
    with pytest.raises(KeyError):
        assert Lowland.set_params(new_params1)
    with pytest.raises(ValueError):
        assert Lowland.set_params(new_params2)


def test_set_population():
    init_herb = [{"species": "Herbivore", "age": 1, "weight": 10.0} for _ in range(10)]

    init_carn = [{"species": "Carnivore", "age": 3, "weight": 14.0} for _ in range(10)]
    l_scape = Landscape()
    l_scape.set_population(init_herb)
    l_scape.set_population(init_carn)
    assert type(l_scape.herbivore_list[0]) == Herbivore
    assert type(l_scape.carnivore_list[0]) == Carnivore
    assert len(l_scape.herbivore_list) == 10
    assert len(l_scape.carnivore_list) == 10


def test_add_population():
    l_scape = Landscape()
    l_scape.add_population(Herbivore(5, 20))
    l_scape.add_population(Carnivore(5, 20))
    assert len(l_scape.herbivore_list) == 1
    assert len(l_scape.carnivore_list) == 1


def test_food_grows_lowland():
    l_scape = Lowland()
    l_scape.available_food = 0
    l_scape.food_grows()

    assert l_scape.available_food != 0
    assert l_scape.available_food == 800


def test_food_grows_highland():
    l_scape = Highland()
    l_scape.available_food = 0
    l_scape.food_grows()

    assert l_scape.available_food != 0
    assert l_scape.available_food == 300


def test_animal_eats():
    l_scape = Landscape()


def test_reproduce_herbivore(mocker):
    mocker.patch('numpy.random.random', return_value=0.00001)
    init_pop = [{"species": "Herbivore", "age": 3, "weight": 50.0},
                {"species": "Herbivore", "age": 3, "weight": 54.0},
                {"species": "Herbivore", "age": 3, "weight": 50.0},
                {"species": "Herbivore", "age": 3, "weight": 54.0}]

    l_scape = Landscape()
    l_scape.set_population(init_pop)

    l_scape.herbivore_reproduce()

    assert len(l_scape.herbivore_list) != 4
    assert len(l_scape.herbivore_list) == 8


def test_reproduce_carnivore(mocker):
    mocker.patch('numpy.random.random', return_value=0.00001)
    init_pop = [{"species": "Carnivore", "age": 3, "weight": 50.0},
                {"species": "Carnivore", "age": 3, "weight": 54.0},
                {"species": "Carnivore", "age": 3, "weight": 50.0},
                {"species": "Carnivore", "age": 3, "weight": 54.0}]

    l_scape = Landscape()
    l_scape.set_population(init_pop)

    l_scape.carnivore_reproduce()

    assert len(l_scape.carnivore_list) != 4
    assert len(l_scape.carnivore_list) == 8


def test_animals_die():
    init_pop = [{"species": "Herbivore", "age": 1, "weight": 10.0} for _ in range(10)] + \
               [{"species": "Carnivore", "age": 3, "weight": 14.0} for _ in range(10)]
    l_scape = Landscape()
    l_scape.set_population(init_pop)

    old_pop = l_scape.carnivore_list + l_scape.herbivore_list
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
