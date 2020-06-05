# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

import random
from .animals import Herbivore, Carnivore

"""
Here we will  
"""
"Break for loop if fodder is empty."
"""
Defines the order of what happens in a year:
1. Food grows and they feed (Herbivores then carnivores)
2. They procreate based on probability and fitness
3. They migrate (Will wait with this)
4. They age
5. They loose weight according to parameters
6. Some die based on probability and fitness

"""

"if birth_weight_loss >=  self.weight:"
"     No birth"
"Else: "
"     new_born = animal.Herbivore"
"     mother_weight = animal.params['xi'] * new_born.weight"


class Landscape:
    keys = ['L', 'W', 'H', 'D']
    params = dict.fromkeys(keys)

    @classmethod
    def set_params(cls, new_params):
        for key in Landscape.keys:

        pass


    def __init__(self, f_max):
        "common traits are size."

        self.f_max = f_max

        self.animals = list()
        pass


class Lowland(Landscape):
    passable = True

    def __init__(self, f_max):
        super().__init__(f_max)
    "Make function for available fodder and population growth"


class Highland(Landscape):
    passable = True

    def __init__(self, f_max):
        super().__init__(f_max)


class Water(Landscape):
    passable = False

    def __init__(self):
        super().__init__(f_max=0)


class Desert(Landscape):
    passable = True

    def __init__(self):
        super().__init__(f_max=0)
