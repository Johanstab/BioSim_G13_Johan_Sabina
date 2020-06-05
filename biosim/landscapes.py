# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

import random
import numpy as np
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
        self.population = {'Herbivore': [], 'Carnivore': []}
        self.available_food = 0

    def food_grows(self):
        self.available_food = self.f_max

    def animals_eat(self):

        np.random.shuffle(self.population['Herbivore'])

        for herbivore in self.population['Herbivore']:
            if self.available_food <= 0:
                break
            else:
                herbivore.eats(Landscape)

    def animals_reproduce(self):
        nr_animals = len(self.population['Herbivore'])
        if nr_animals < 2:
            return False
        for herbivore in self.population['Herbivore']:
            if herbivore.weight < herbivore.params['zeta'] * (
                    herbivore.params['w_birth'] + herbivore.params['sigma_birth']):
                break
            if herbivore.birth(nr_animals):
                self.population['Herbivore'].append(Herbivore)

    def animals_die(self):
        death_list_herb = []

        for herbivore in self.population['Herbivore']:
            if herbivore.death_probability():
                death_list_herb.append(herbivore)

    def animals_age(self):
        for herbivore in self.population['Herbivore']:
            herbivore.aging()

    def animals_lose_weight(self):
        for herbivore in self.population['Herbivore']:
            herbivore.weight_loss()




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
