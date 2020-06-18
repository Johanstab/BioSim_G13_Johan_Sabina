# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import pytest
import scipy.stats as stats
import numpy as np
np.random.seed(1)
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


def test_set_params_key_error():
    new_params = {'birth': 12.0}

    with pytest.raises(KeyError):
        Animals.set_params(new_params)


def test_set_params_value_error():
    new_params_1 = {'eta': 5}
    new_params_2 = {'DeltaPhiMax': 0}
    new_params_3 = {'F': -5}

    with pytest.raises(ValueError):
        Herbivore.set_params(new_params_1)

    with pytest.raises(ValueError):
        Herbivore.set_params(new_params_2)

    with pytest.raises(ValueError):
        Herbivore.set_params(new_params_3)


def test_init():
    """
    Test that the init method works for both carnivores and herbivores.
    """
    carn = Carnivore(3, 40)
    herb = Herbivore(2, 27)

    herb.set_params({
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

    assert carn.weight == 40
    assert carn.age == 3

    assert herb.weight == 27
    assert herb.age == 2


def test_constructor_default():
    """Default constructor callable."""
    assert isinstance(Herbivore(), Herbivore)
    assert isinstance(Carnivore(), Carnivore)


def test_age():
    """
    Test that it is possible to set and get the age of animals.
    """
    herb = Herbivore(10, 20)
    carn = Carnivore(10, 20)
    assert herb.age == 10
    assert carn.age == 10

    herb.age = 12
    carn.age = 12
    assert herb.age == 12
    assert carn.age == 12


def test_ageing():
    """

    Test that the both herbivore and carnivore ages the right way.
    """
    herb = Herbivore(10, 20)
    carn = Carnivore(10, 20)

    herb.aging()
    carn.aging()
    assert herb.age == 11
    assert carn.age == 11


def test_value_error_for_age_and_weight():
    with pytest.raises(ValueError):
        Herbivore(age=-9)

    with pytest.raises(ValueError):
        Herbivore(weight=-4)

    with pytest.raises(ValueError):
        Carnivore(age=-40)

    with pytest.raises(ValueError):
        Carnivore(weight=-8)


def test_weight():
    """
    Tests that it is possible to set and get weight of an animal.

    """
    herb = Herbivore(10, 20)
    carn = Carnivore(10, 20)

    assert herb.weight == 20
    assert carn.weight == 20

    herb.weight = 30
    carn.weight = 30
    assert herb.weight == 30
    assert carn.weight == 30


def test_weight_loss():
    """
    Test that the animals loses weight for every year
    """
    herb = Herbivore(9, 30)
    herb.weight_loss()

    carn = Carnivore(9, 40)
    carn.weight_loss()

    assert herb.weight != 30
    assert herb.weight == 28.5

    assert carn.weight != 40
    assert carn.weight == 35


def test_weight_gain_eating_herbivore():
    """
    Test that the animals gains the right amount of weight after eating"
    """

    herb = Herbivore(5, 10)

    herb.eats(10)

    assert herb.weight != 10
    assert herb.weight == 19


def test_weight_gain_eating_carnivore(mocker):
    mocker.patch('numpy.random.random', return_value=0.0000001)
    carn = Carnivore(5, 20)
    herb = [Herbivore(6, 20)]
    herb = carn.eat(herb)
    assert carn.weight != 20
    assert carn.weight == 35

    assert herb == []


def test_eat_if_eaten(mocker):
    mocker.patch('numpy.random.random', return_value=0.000001)
    carn = Carnivore(5, 20)
    herbs = [Herbivore(6, 20), Herbivore(6, 20), Herbivore(6, 20)]
    carn.eat(herbs)
    assert carn.weight == 57.5


def test_eat_if_deltaphimax_low(mocker):
    mocker.patch('numpy.random.random', return_value=0.000001)
    carn = Carnivore(5, 20)
    herb = [Herbivore(6, 20)]
    carn.set_params({'DeltaPhiMax': 0.0001})
    carn.eat(herb)
    assert carn.weight != 20
    assert carn.weight == 35


def test_eat_if_eaten_more_that_deltaphimax(mocker):
    mocker.patch('numpy.random.random', return_value=0.0000001)
    carn = Carnivore(5, 20)
    herbs = [Herbivore(6, 20), Herbivore(6, 20), Herbivore(6, 20)]
    carn.eat(herbs)
    assert carn.weight == 57.5


def test_eat_enough():
    carn = Carnivore(5, 20)
    carn_weight = carn.weight
    herbs = [Herbivore(6, 20), Herbivore(6, 20), Herbivore(6, 20)]
    carn.set_params({"F": 0})

    assert carn.eat(herbs)
    assert carn.weight == carn_weight


def test_fitness_herb_more_than_carn():
    carn = Carnivore(2, 5)
    carn_weight = carn.weight
    herb = [Herbivore(6, 25), Herbivore(6, 25), Herbivore(6, 25)]

    assert carn.eat(herb)
    assert carn_weight == carn.weight


def test_birth_weight():
    weight_birth = Herbivore.weight_birth(5, 1.5)

    assert weight_birth > 0


def test_fitness_aging():
    """
    Testing that the fitness function works, that the fitness changes when animal aging
    """
    herb = Herbivore(5, 10)
    fitness_before_herbivore = herb.fitness

    carn = Carnivore(5, 30)
    fitness_before_carnivore = carn.fitness

    herb.aging()
    carn.aging()

    fitness_after_herbivore = herb.fitness
    fitness_after_carnivore = carn.fitness

    assert fitness_before_herbivore != fitness_after_herbivore
    assert fitness_before_carnivore != fitness_after_carnivore


def test_fitness_weight_loss():
    herb = Herbivore(5, 10)
    fitness_before_herbivore = herb.fitness

    carn = Carnivore(5, 30)
    fitness_before_carnivore = carn.fitness

    herb.weight_loss()
    carn.weight_loss()

    fitness_after_herbivore = herb.fitness
    fitness_after_carnivore = carn.fitness

    assert fitness_before_herbivore != fitness_after_herbivore
    assert fitness_before_carnivore != fitness_after_carnivore


def test_fitness_weight_zero():
    herb = Herbivore(5, 0)
    carn = Carnivore(5, 0)
    assert herb.fitness == 0
    assert carn.fitness == 0


def test_fitness_function():
    """
    Testing if the fitness is calculated the right way
    """
    herb = Herbivore(5, 10)
    carn = Carnivore(5, 20)

    assert herb.fitness == 0.49999999962087194
    assert carn.fitness == 0.998313708904945


def test_p_function():
    herb_q = Herbivore.q(1, 1, 0.5, 0.5)
    carn_q = Carnivore.q(1, 1, 0.5, 0.5)
    assert herb_q == 0.43782349911420193
    assert carn_q == 0.43782349911420193


def test_death_weight():
    """
    Testing that the animal dies if the weight is zero
    """

    herb = Herbivore(3, 0)
    carn = Carnivore(5, 0)

    assert herb.death() is True
    assert carn.death() is True


def test_death_probability(mocker):
    mocker.patch('numpy.random.random', return_value=0.000001)
    herb = Herbivore(5, 10)
    carn = Carnivore(6, 15)
    assert herb.death() is True
    assert carn.death() is True

    mocker.patch('numpy.random.random', return_value=1)
    herb = Herbivore(5, 10)
    carn = Carnivore(6, 15)
    assert herb.death() is False
    assert carn.death() is False


def test_birth(mocker):
    """
    Test that the animals can't reproduce if only one animal is present"
    """
    mocker.patch('numpy.random.random', return_value=0.000001)
    herb = Herbivore(5, 35)
    carn = Carnivore(5, 30)
    nr_animals = 10

    assert herb.birth(nr_animals) is not None
    assert carn.birth(nr_animals) is not None

    mocker.patch('numpy.random.random', return_value=1)
    herb = Herbivore(5, 35)
    carn = Carnivore(5, 30)
    nr_animals = 10

    assert herb.birth(nr_animals) is None
    assert carn.birth(nr_animals) is None


def test_no_birth_weight_to_low():
    herb = Herbivore(5, 15)
    carn = Carnivore(5, 15)
    nr_animals = 2

    assert herb.birth(nr_animals) is None
    assert carn.birth(nr_animals) is None


def test_no_birth_baby_to_heavy(mocker):
    mocker.patch('numpy.random.normal', return_value=50)
    mocker.patch('numpy.random.random', return_value=0.00001)
    herb = Herbivore(5, 35)
    carn = Carnivore(5, 30)
    nr_animals = 10

    assert herb.birth(nr_animals) is None, 'Animal should not give birth if weight of baby > mother'
    assert carn.birth(nr_animals) is None, 'Animal should not give birth if weight of baby > mother'


def test_no_birth_probability(mocker):
    mocker.patch('numpy.random.random', return_value=1)
    herb = Herbivore(5, 35)
    carn = Carnivore(5, 30)
    nr_animals = 10

    assert herb.birth(nr_animals) is None
    assert carn.birth(nr_animals) is None


def test_mother_loose_weight(mocker):
    mocker.patch('numpy.random.normal', return_value=20)
    mocker.patch('numpy.random.random', return_value=0.00001)
    herbivore = Herbivore(5, 35)
    carnivore = Carnivore(5, 30)
    nr_animals = 10

    new_herb = herbivore.birth(nr_animals)
    new_carn = carnivore.birth(nr_animals)

    assert herbivore.weight == 11
    assert carnivore.weight == 8
    assert new_herb.age == 0, 'New baby should be age zero'
    assert new_carn.age == 0, 'New baby should be age zero'


def test_gaussian_distribution_birth():
    """Test if the birth weight of new Animals is has gaussian distribution.
    Hypothesis: p > 0.05 : Likely that the it is a gaussian distribution.
                p < 0.05 : Probably not a gaussian distribution.

    Also tests that the std of carnivores and herbivores is approximately
    equal to the parameters.
    """
    herbs = [Herbivore() for _ in range(10000)]
    herbs_weight = [herb.weight for herb in herbs]
    herbs_std = np.std(herbs_weight)
    carns = [Carnivore() for _ in range(10000)]
    carns_weight = [carn.weight for carn in carns]
    carns_std = np.std(carns_weight)

    stat_herb, p_herb = stats.normaltest(herbs_weight)
    stat_carn, p_carn = stats.normaltest(carns_weight)

    assert p_herb > 0.05
    assert p_carn > 0.05
    assert carns_std == pytest.approx(Carnivore.params['sigma_birth'], rel=1e-2, abs=1e-10)
    assert herbs_std == pytest.approx(Herbivore.params['sigma_birth'], rel=1e-2, abs=1e-10)


def test_move(mocker):
    mocker.patch('numpy.random.random', return_value=0.0000001)
    herbivore = Herbivore(5, 20)
    carnivore = Carnivore(5, 20)

    assert herbivore.move() is True
    assert carnivore.move() is True

    mocker.patch('numpy.random.random', return_value=1)
    herbivore = Herbivore(5, 20)
    carnivore = Carnivore(5, 20)

    assert herbivore.move() is False
    assert carnivore.move() is False


def test_reset_move():
    herb = Herbivore(5, 20)
    herb.has_moved = True
    herb.reset_has_moved()
    assert herb.has_moved is False
