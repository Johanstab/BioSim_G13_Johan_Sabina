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
    keys = ['f_max']
    params = dict.fromkeys(keys)

    @classmethod
    def set_params(cls, new_params):

        if new_params[0] not in Landscape.keys:
            raise KeyError('Invalid parameter name: ' + new_params[0])

        if new_params == 'f_max' and new_params['f_max'] < 0:
            raise ValueError('f_max must be positive')

        cls.params = new_params

    def __init__(self):
        "common traits are size."

        self.f_max = self.params['f_max']

        self.animals_herbi = []
        self.animals_carni = []
        self.available_food = 0
        self.left_overs = 0

    def food_grows(self):
        self.available_food = self.f_max

    def animals_eat(self):

    def animals_reproduce(self):

    def animals_die(self):

    def animals_age(self):




class Lowland(Landscape):
    param = {'f_max': 800}
    passable = True

    def __init__(self):
        super().__init__()
        self.f_max = self.params['f_max']

    "Make function for available fodder and population growth"


class Highland(Landscape):
    param = {'f_max': 300}
    passable = True

    def __init__(self):
        super().__init__()
        self.f_max = self.params['f_max']


class Water(Landscape):
    passable = False

    def __init__(self):
        super().__init__(f_max=0)


class Desert(Landscape):
    passable = True

    def __init__(self):
        super().__init__(f_max=0)
