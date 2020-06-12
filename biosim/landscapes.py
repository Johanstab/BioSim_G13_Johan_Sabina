# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"


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
        self.herbivore_list = []
        self.sorted_herbi = []
        self.sorted_carni = []
        self.carnivore_list = []
        self.available_food = 0

    def set_population(self, input_dict):
        """Sets the populations of animals.

        Parameters
        ----------
        input_dict : dict
                Dictionary containing Herbivores and Carnivores.

        Returns
        -------
        None
        """
        for animal in input_dict:
            if animal["species"] == "Herbivore":
                self.herbivore_list.append(Herbivore(age=animal["age"], weight=animal["weight"]))
            else:
                self.carnivore_list.append(Carnivore(age=animal["age"], weight=animal["weight"]))

    def food_grows(self):
        """Updates food for each year."""
        self.available_food = self.f_max

    def herbivore_eats(self):
        """Cycle where all herbivores eats fodder in a random order according to how much
        the parameters defines. If there is no fodder left then no more herbivores get to eat.

        Returns
        -------
        None
        """
        np.random.shuffle(self.herbivore_list)

        for herbivore in self.herbivore_list:
            if self.available_food == 0:
                break
            if self.available_food >= herbivore.params['F']:
                herbivore.eats(herbivore.params['F'])
                self.available_food -= herbivore.params['F']
            if self.available_food < herbivore.params['F']:
                herbivore.eats(self.available_food)
                self.available_food = 0

    def carnivore_eats(self):
        """Cycle where all carnivores eats herbivores. The fittest carnivore tries to kill the
        least fit herbivore and continues until it has eaten according to the parameters. When
        the fittest carnivore has is satisfied the next in order of fitness will proceed until
        until everyone is satisfied or all herbivores are killed.

        Returns
        -------
        None
        """
        self.carnivore_list.sort(key=lambda animal: animal.fitness, reverse=True)
        self.herbivore_list.sort(key=lambda animal: animal.fitness)

        for carnivore in self.carnivore_list:
            dead = carnivore.eat(self.herbivore_list)
            self.herbivore_list.remove(dead)

    def herbivore_reproduce(self):
        """

        Returns
        -------

        """
        nr_animals = len(self.herbivore_list)

        if nr_animals < 2:
            return False

        new_babies = []
        for herbivore in self.herbivore_list:
            new_baby = herbivore.birth(nr_animals)
            if new_baby is not None:
                new_babies.append(new_baby)

        self.herbivore_list.extend(new_babies)

    def carnivore_reproduce(self):
        """

        Returns
        -------

        """
        nr_animals = len(self.carnivore_list)

        if nr_animals < 2:
            return False

        new_babies = []
        for carnivore in self.carnivore_list:
            new_baby = carnivore.birth(nr_animals)
            if new_baby is not None:
                new_babies.append(new_baby)

        self.carnivore_list.extend(new_babies)

    def animals_die(self):
        """Checks if a animal should die or not and removes the dead animal from the lists.

        Returns
        -------
        None
        """
        self.herbivore_list = [animal for animal in self.herbivore_list if not animal.death()]
        self.carnivore_list = [animal for animal in self.carnivore_list if not animal.death()]

    def animals_age(self):
        """The animals increase one year in age"""
        for herbivore in self.herbivore_list:
            herbivore.aging()
        for carnivore in self.carnivore_list:
            carnivore.aging()

    def animals_lose_weight(self):
        """The animals loose weight"""
        for herbivore in self.herbivore_list:
            herbivore.weight_loss()
        for carnivore in self.carnivore_list:
            carnivore.weight_loss()

    def animal_migrate(self, map):
        animal_list = self.carnivore_list + self.herbivore_list
        for animals in animal_list:
            if animals.has_moved is not True:
                if animals.move:


class Lowland(Landscape):
    params = {"f_max": 800}
    passable = True

    def __init__(self):
        super().__init__()
        self.f_max = self.params["f_max"]

    "Make function for available fodder and population growth"


class Highland(Landscape):
    params = {"f_max": 300}
    passable = True

    def __init__(self):
        super().__init__()
        self.f_max = self.params["f_max"]


class Water(Landscape):
    passable = False

    def __init__(self):
        super().__init__()


class Desert(Landscape):
    params = {"f_max": 0}
    passable = True

    def __init__(self):
        super().__init__()
        self.f_max = self.params['f_max']
