# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

import pytest
from biosim.animals import Herbivore, Carnivore
from biosim.landscapes import Lowland
import biosim.island


class TestAnimal:

    @pytest.fixture()
    def creat_herb(self):
        """Creates a Herbivore object"""
        herb = Herbivore(5, 10)
        return herb

    def herb_eat_and_gain_weight(self):
        pass

    def herb_loses_weight(self):
        pass

    def herb_aging(self):
        pass

    def test_herb_not_dead(self,create_herb):
        """ New animal should not be dead"""

        assert create_herb.is_dead is False, "Animal should not be dead"


    def herb_age_zero_birth(self):
        pass