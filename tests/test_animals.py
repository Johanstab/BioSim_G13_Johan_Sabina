# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

import pytest
from biosim.animals import Herbivore, Carnivore
from biosim.landscapes import Lowland
import biosim.island


class TestAnimal:

    @pytest.fixture()
    def create_herb(self):
        """Creates a Herbivore object"""
        herb = Herbivore(5, 10)
        return herb

    def herb_eat_and_gain_weight(self, create_herb):
        """Herbivores weight should increase when eating"""
        prev_weigth = create_herb.eats(Lowland)

    def herb_loses_weight(self):
        pass

    def herb_aging(self):
        pass


    def herb_age_zero_birth(self):
        pass