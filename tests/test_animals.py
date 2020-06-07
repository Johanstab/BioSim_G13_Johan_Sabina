# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

import pytest
from biosim.animals import Herbivore, Carnivore
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
    Test that the animals ages the right way
    """
    herbivore = Herbivore(10, 20)
    assert herbivore.age == 10

    herbivore.aging()
    assert herbivore.age == 11


def test_weight_loss():
    herbivore = Herbivore(9, 30)
    herbivore.weight_loss()

    assert not herbivore.weight == 30
    assert herbivore.weight == 28.5


def test_weight_gain():
    herbivore = Herbivore(15, 20)

    assert not herbivore.weight == 20
    assert herbivore.weight == 29


def test_death():







