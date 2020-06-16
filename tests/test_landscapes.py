# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import pytest
from biosim.landscapes import Landscape, Lowland, Highland, Desert, Water
from biosim.animals import Herbivore, Carnivore


def test_set_params():
    l_scape = Lowland()
    params = l_scape.params
    new_params = {'f_max': 5000}
    new_params = l_scape.set_params(new_params)
    assert params != new_params

    l_scape.set_params({'f_max': 800})


def test_init_landscapes():
    lowland = Lowland()
    highland = Highland()
    water = Water()
    desert = Desert()
    assert type(lowland) == Lowland
    assert type(highland) == Highland
    assert type(water) == Water
    assert type(desert) == Desert



def test_food_grows_lowland():
    l_scape = Lowland()
    l_scape.available_food = 0
    l_scape.food_grows()

    assert l_scape.available_food != 0
    assert l_scape.available_food == 800


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


def test_food_grows_highland():
    l_scape = Highland()
    l_scape.available_food = 0
    l_scape.food_grows()

    assert l_scape.available_food != 0
    assert l_scape.available_food == 300


def test_herbivore_eats():
    ini_pop = [{"species": "Herbivore", "age": 3, "weight": 20.0},
                {"species": "Herbivore", "age": 3, "weight": 20.0}]
    l_scape = Lowland()
    l_scape.set_population(ini_pop)
    l_scape.food_grows()

    weight_before = l_scape.herbivore_list[0].weight
    l_scape.herbivore_eats()
    assert weight_before != l_scape.herbivore_list[0].weight


def test_herbivore_does_not_eat():
    ini_pop = [{"species": "Herbivore", "age": 3, "weight": 20.0},
                {"species": "Herbivore", "age": 3, "weight": 20.0}]
    l_scape = Lowland()
    l_scape.set_population(ini_pop)
    l_scape.available_food = 0
    weight_before = l_scape.herbivore_list[0].weight
    l_scape.herbivore_eats()
    assert weight_before == l_scape.herbivore_list[0].weight


def test_herbivore_eats_available_food():
    ini_pop = [{"species": "Herbivore", "age": 3, "weight": 20.0},
                {"species": "Herbivore", "age": 3, "weight": 20.0}]
    l_scape = Lowland()
    l_scape.set_population(ini_pop)
    l_scape.available_food = 10
    l_scape.herbivore_eats()
    weight = l_scape.herbivore_list[0].weight + l_scape.herbivore_list[1].weight
    assert weight == 49
    assert l_scape.available_food == 0


def test_carnivore_eats():
    ini_pop = [{"species": "Herbivore", "age": 3, "weight": 10.0} for _ in range(10)] + \
               [{"species": "Carnivore", "age": 3, "weight": 14.0} for _ in range(10)]
    l_scape = Desert()
    l_scape.set_population(ini_pop)
    carns  = l_scape.carnivore_list
    herbs = l_scape.herbivore_list
    l_scape.carnivore_eats()
    assert herbs != l_scape.herbivore_list
    assert carns == l_scape.carnivore_list


def test_no_reproduce_one_animal():
    ini_pop = [{"species": "Herbivore", "age": 1, "weight": 10.0} for _ in range(1)] + \
              [{"species": "Carnivore", "age": 3, "weight": 14.0} for _ in range(1)]
    l_scape = Lowland()
    l_scape.set_population(ini_pop)
    assert l_scape.herbivore_reproduce() is False
    assert l_scape.carnivore_reproduce() is False


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


def test_animals_die(mocker):
    mocker.patch('numpy.random.random', return_value=0)
    init_pop = [{"species": "Herbivore", "age": 1, "weight": 15.0} for _ in range(10)] + \
               [{"species": "Carnivore", "age": 3, "weight": 15.0} for _ in range(10)]
    l_scape = Landscape()
    l_scape.set_population(init_pop)

    old_pop = l_scape.carnivore_list + l_scape.herbivore_list
    l_scape.animals_die()

    new_pop = (l_scape.carnivore_list + l_scape.herbivore_list)

    assert old_pop != new_pop


def test_animals_age():
    init_pop = [{"species": "Herbivore", "age": 1, "weight": 10.0} for _ in range(10)] + \
               [{"species": "Carnivore", "age": 3, "weight": 14.0} for _ in range(10)]
    l_scape = Landscape()
    l_scape.set_population(init_pop)

    age_before_herb = l_scape.herbivore_list[0].age
    age_before_carn = l_scape.carnivore_list[0].age

    l_scape.animals_age()

    age_after_herb = l_scape.herbivore_list[0].age
    age_after_carn = l_scape.carnivore_list[0].age

    assert age_after_carn != age_before_carn
    assert age_after_herb != age_before_carn
    assert age_after_carn == age_before_carn + 1
    assert age_after_herb == age_before_herb + 1


def test_animals_weight_loss():
    init_pop = [{"species": "Herbivore", "age": 1, "weight": 10.0} for _ in range(10)] + \
               [{"species": "Carnivore", "age": 3, "weight": 14.0} for _ in range(10)]
    l_scape = Landscape()
    l_scape.set_population(init_pop)

    herb_weight = l_scape.herbivore_list[0].weight
    carn_weight = l_scape.carnivore_list[0].weight

    l_scape.animals_lose_weight()

    new_herb_weight = l_scape.herbivore_list[0].weight
    new_carn_weight = l_scape.carnivore_list[0].weight

    assert herb_weight != new_herb_weight
    assert carn_weight != new_carn_weight
    assert new_carn_weight == 12.25
    assert new_herb_weight == 9.5


def test_migrate(mocker):
    mocker.patch('numpy.random.random', return_value=0)
    init_pop = [{"species": "Herbivore", "age": 1, "weight": 10.0} for _ in range(10)] + \
               [{"species": "Carnivore", "age": 3, "weight": 14.0} for _ in range(10)]
    l_scape = Lowland()
    l_scape.set_population(init_pop)
    herbs, carns = l_scape.animals_migrate()
    assert herbs != []
    assert carns != []
    assert herbs == l_scape.herbivore_list
    assert carns == l_scape.carnivore_list


def test_reset_migrate(mocker):
    mocker.patch('numpy.random.random', return_value=0)
    init_pop = [{"species": "Herbivore", "age": 1, "weight": 10.0} for _ in range(10)] + \
               [{"species": "Carnivore", "age": 3, "weight": 14.0} for _ in range(10)]
    l_scape = Lowland()
    l_scape.set_population(init_pop)
    herbs, carns = l_scape.animals_migrate()
    herb_moved = herbs[0].has_moved
    carn_moved = carns[0].has_moved
    l_scape.reset_migrate()
    assert herb_moved is False
    assert carn_moved is False
