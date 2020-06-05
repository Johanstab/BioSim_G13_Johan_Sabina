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


class Landscapes:
    def __init__(self, row, columns, f_max):
        "common traits are size."
        pass


class Lowland(Landscapes):
    passable = True
    f_max = 800.0

    def __init__(self):
        super().__init__()
    "Make function for available fodder and population growth"


class Highland(Landscapes):
    passable = True
    f_max = 300.0

    def __init__(self):
        super().__init__()


class Water(Landscapes):
    passable = False

    def __init__(self):
        super().__init__()


class Desert(Landscapes):
    passable = True
    f_max = 0

    def __init__(self):
        super().__init__()
