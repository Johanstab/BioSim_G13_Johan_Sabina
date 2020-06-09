# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

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


class Landscape:
    keys = ["f_max"]
    params = dict.fromkeys(keys)

    @classmethod
    def set_params(cls, new_params):

        if new_params[0] not in Landscape.keys:
            raise KeyError("Invalid parameter name: " + new_params[0])

        if new_params == "f_max" and new_params["f_max"] < 0:
            raise ValueError("f_max must be positive")

        cls.params = new_params

    def __init__(self):
        "common traits are size."

        self.f_max = self.params["f_max"]
        self.animal_list = []
        self.herbivore_list = []
        self.carnivore_list = []
        self.available_food = 0

    def set_population(self, input_dict):
        for animal in input_dict:
            if animal["species"] == "Herbivore":
                self.herbivore_list.append(Herbivore(age=animal["age"], weight=animal["weight"]))
            else:
                self.animal_list.append(Carnivore(age=animal["age"], weight=animal["weight"]))

    # @property
    # def herbi_list(self):
    #     """List of all herbivore objects in the cell object"""
    #     return [h for h in self.animal_list if type(h).__name__ == "Herbivore"]

    # @property
    # def carn_list(self):
    #     """List of all herbivore objects in the cell object"""
    #     return [c for c in self.animal_list if type(c).__name__ == "Carnivore"]

    def food_grows(self):
        self.available_food = self.f_max

    def animals_eat(self):

        np.random.shuffle(self.herbivore_list)

        for herbivore in self.herbivore_list:
            if self.available_food <= 0:
                break
            else:
                # Rett opp denne
                herbivore.eats(self.available_food)

    def animals_reproduce(self):
        nr_animals = len(self.animal_list)
        if nr_animals < 2:
            return False
        new_babies = []
        # Rette opp denne

        for herbivore in self.herbivore_list:
            if herbivore.birth(nr_animals):
                new_babies.append(Herbivore)

        self.herbivore_list.extend(new_babies)

    def animals_die(self):
        death_list_herbi = []
        #death_list_herbi = []
# Rett opp denne

        for herbivore in self.herbivore_list:
            if herbivore.death():
                death_list_herbi.append(herbivore)

        for dead in death_list_herbi:
            self.herbivore_list.remove(dead)

    def animals_age(self):
        for herbivore in self.herbivore_list:
            herbivore.aging()

    def animals_lose_weight(self):
        for herbivore in self.herbivore_list:
            herbivore.weight_loss()


class Lowland(Landscape):
    param = {"f_max": 800}
    passable = True

    def __init__(self):
        super().__init__()
        self.f_max = self.params["f_max"]

    "Make function for available fodder and population growth"


class Highland(Landscape):
    param = {"f_max": 300}
    passable = True

    def __init__(self):
        super().__init__()
        self.f_max = self.params["f_max"]


class Water(Landscape):
    passable = False

    def __init__(self):
        super().__init__()


class Desert(Landscape):
    passable = True

    def __init__(self):
        super().__init__()
