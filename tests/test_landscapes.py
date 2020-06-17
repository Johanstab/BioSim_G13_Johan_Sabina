# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import pytest
from biosim.landscapes import Landscape, Lowland, Highland, Desert, Water
from biosim.animals import Herbivore, Carnivore


@pytest.fixture(autouse=True)
def test_set_animal_parameters():
    """Sets default parameters to animals for the tests"""
    Herbivore.set_params({
        "w_birth": 8.0,
        "sigma_birth": 1.5,
        "beta": 0.9,
        "eta": 0.05,
        "a_half": 40.0,
        "phi_age": 0.6,
        "w_half": 10.0,
        "phi_weight": 0.1,
        "mu": 0.25,
        "gamma": 0.2,
        "zeta": 3.5,
        "xi": 1.2,
        "omega": 0.4,
        "F": 10.0,
    })
    Carnivore.set_params({
        "w_birth": 6.0,
        "sigma_birth": 1.0,
        "beta": 0.75,
        "eta": 0.125,
        "a_half": 40.0,
        "phi_age": 0.3,
        "w_half": 4.0,
        "phi_weight": 0.4,
        "mu": 0.4,
        "gamma": 0.8,
        "zeta": 3.5,
        "xi": 1.1,
        "omega": 0.8,
        "F": 50.0,
        "DeltaPhiMax": 10.0
    })


@pytest.fixture(autouse=True)
def test_set_params():
    """Sets default parameters to landscapes, and tests that they can be changed."""
    l_scape = Lowland()
    params = l_scape.params
    new_params = {'f_max': 5000}
    new_params = l_scape.set_params(new_params)
    assert params != new_params

    l_scape.set_params({'f_max': 800})
    l_scape2 = Highland()
    l_scape2.set_params({'f_max': 300})


def test_init_landscapes():
    """Test that landscapes can be initialised."""
    lowland = Lowland()
    highland = Highland()
    water = Water()
    desert = Desert()
    assert isinstance(lowland, Lowland)
    assert isinstance(highland, Highland)
    assert isinstance(water, Water)
    assert isinstance(desert, Desert)


def test_food_grows_lowland():
    """Test that fodder will grow in Lowland"""
    l_scape = Lowland()
    l_scape.available_food = 0
    l_scape.food_grows()

    assert l_scape.available_food != 0
    assert l_scape.available_food == 800


def test_set_params_error():
    """Test if error is raised when invalid key or value is past/used."""
    new_params1 = {'fodder_max': 10}
    new_params2 = {'f_max': -10}
    with pytest.raises(KeyError):
        assert Lowland.set_params(new_params1)
    with pytest.raises(ValueError):
        assert Lowland.set_params(new_params2)


def test_set_population():
    """Test that population can be set in landscapes"""
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
    """Test if population can be added to landscapes"""
    l_scape = Landscape()
    l_scape.add_population(Herbivore(5, 20))
    l_scape.add_population(Carnivore(5, 20))
    assert len(l_scape.herbivore_list) == 1
    assert len(l_scape.carnivore_list) == 1


def test_food_grows_highland():
    """Test that fodder will grow in Lowland"""
    l_scape = Highland()
    l_scape.available_food = 0
    l_scape.food_grows()

    assert l_scape.available_food != 0
    assert l_scape.available_food == 300


def test_herbivore_eats():
    """Test that the herbivore eats, by checking if it gains weight or not"""
    ini_pop = [{"species": "Herbivore", "age": 3, "weight": 20.0},
               {"species": "Herbivore", "age": 3, "weight": 20.0}]
    l_scape = Lowland()
    l_scape.set_population(ini_pop)
    l_scape.food_grows()

    weight_before = l_scape.herbivore_list[0].weight
    l_scape.herbivore_eats()
    assert weight_before != l_scape.herbivore_list[0].weight


def test_herbivore_does_not_eat():
    """Test that the herbivore do not eat, by checking if its weight stays the same"""
    ini_pop = [{"species": "Herbivore", "age": 3, "weight": 20.0},
               {"species": "Herbivore", "age": 3, "weight": 20.0}]
    l_scape = Lowland()
    l_scape.set_population(ini_pop)
    l_scape.available_food = 0
    weight_before = l_scape.herbivore_list[0].weight
    l_scape.herbivore_eats()
    assert weight_before == l_scape.herbivore_list[0].weight


def test_herbivore_eats_available_food():
    """Test that the herbivore only eats whats available of food, by checking the total weight
    of the present herbivores and that available food becomes 0"""
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
    """Test that the carnivores eats, by checking if the amount of herbivores are different before
    and after carnivores eats"""
    ini_pop = [{"species": "Herbivore", "age": 3, "weight": 10.0} for _ in range(10)] + \
              [{"species": "Carnivore", "age": 3, "weight": 14.0} for _ in range(10)]
    l_scape = Desert()
    l_scape.set_population(ini_pop)
    carns = l_scape.carnivore_list
    herbs = l_scape.herbivore_list
    l_scape.carnivore_eats()
    assert herbs != l_scape.herbivore_list
    assert carns == l_scape.carnivore_list


def test_no_reproduce_one_animal():
    """Test that no reproducing will happen when only on animal for the species is present."""
    ini_pop = [{"species": "Herbivore", "age": 1, "weight": 10.0} for _ in range(1)] + \
              [{"species": "Carnivore", "age": 3, "weight": 14.0} for _ in range(1)]
    l_scape = Lowland()
    l_scape.set_population(ini_pop)
    assert l_scape.herbivore_reproduce() is False
    assert l_scape.carnivore_reproduce() is False


def test_reproduce_herbivore(mocker):
    """Test that the herbivore reproduce when there is more than one herbivore present."""
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
    """Test that the carnivore reproduce when there is more than one carnivore present."""
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
    """Test if the animals actually die for random probability."""
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
    """Test that the animals ages the right way."""
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
    """Test that the animal loses weight naturally."""
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
    """Test that the animals migrate for on cell to another"""
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
    """"""
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
