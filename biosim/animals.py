# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import numpy as np
import random as random


class Animals:
    "Move params to different species and create a set_params method"
    keys = [
        "w_birth",
        "sigma_birth",
        "beta",
        "eta",
        "a_half",
        "phi_age",
        "w_half",
        "phi_weight",
        "mu",
        "gamma",
        "zeta",
        "xi",
        "omega",
        "F",
        "DeltaPhiMax",
    ]
    params = dict.fromkeys(keys)

    @classmethod
    def set_params(cls, new_params):
        for key in new_params:
            if key not in Animals.keys:
                raise KeyError("Invalid parameter name: " + key)

        for iterator in new_params:
            if iterator == "eta" and new_params[iterator] >= 1:
                raise ValueError("eta must be <= 1.")
            if iterator == "DeltaPhiMax" and new_params[iterator] <= 0:
                raise ValueError("DeltaPhiMax must be positive!")
            if new_params[iterator] < 0:
                raise ValueError("{} cannot be negative".format(iterator))
            cls.params[iterator] = new_params[iterator]
            # Implementer en metode med dict.update

    def __init__(self, age=0, weight=None):
        self._age = age
        self.weight = weight
        self.phi = 0
        self.prob_death = 0

        if self.weight is None:
            self.weight = self.weight_birth(self.params["w_birth"], self.params["sigma_birth"])

    @staticmethod
    def weight_birth(weight, sigma):
        """

        Parameters
        ----------
        weight : float

        sigma : float

        Returns
        -------

        """
        return np.random.normal(weight, sigma)

    @property
    def age(self):
        """

        Returns
        -------

        """
        return self._age

    def aging(self):
        """

        Returns
        -------

        """
        self._age += 1

    def weight_loss(self):
        """

        Returns
        -------

        """
        self.weight -= self.params["eta"] * self.weight
        return self.weight

    @staticmethod
    def q(sgn, x, x_half, phi):
        """

        Parameters
        ----------
        sgn : int
            Positive or negative defining which part of the function it is
        x  : int
            The age or weight of the animal
        x_half  : float
            The mean weight or life expectancy of an animal(set parameter)
        phi  : float
            WRITE MORE EXPLANATION HERE!

        Returns
        -------
        float
            The q value later used to determine fitness
        """
        return 1.0 / (1.0 + np.exp(sgn * phi * (x - x_half)))

    @property
    def fitness(self):
        """

        Returns
        -------
        float
            The generated fitness of the animal.
        """
        if self.weight <= 0:
            self.phi = 0
        else:
            self.phi = Animals.q(
                +1, self.age, self.params["a_half"], self.params["phi_age"]
            ) * Animals.q(-1, self.weight, self.params["w_half"], self.params["phi_weight"])
        return self.phi

    def birth(self, nr_animals):
        """

        Parameters
        ----------
        nr_animals : int
                The number of same sex animals in the cell.

        Returns
        -------
        bool
            Determining if there should be born a baby or not.
        """
        # if type(self) is not Herbivore or Carnivore:
        #     raise TypeError('This type is not valid in this simulation')

        if self.weight < self.params["zeta"] * (
                self.params["w_birth"] + self.params["sigma_birth"]):
            return False

        b_prob = min(1, self.params["gamma"] * self.fitness * (nr_animals - 1))

        if random.random() < b_prob:
            if type(self) is Herbivore:
                new_baby = Herbivore()
            else:
                new_baby = Carnivore()
            if new_baby.weight * self.params['xi'] < self.weight:
                self.weight -= new_baby.weight * self.params['xi']
                return new_baby

    def death(self):
        if self.weight == 0:
            return True

        prob_death = self.params['omega'] * (1 - self.fitness)
        return random.random() < prob_death


class Herbivore(Animals):
    params = {
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
    }

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)

    def eats(self, cell):
        self.weight += cell * self.params['beta']


class Carnivore(Animals):
    params = {
        "w_birth": 6.0,
        "sigma_birth": 1.0,
        "beta": 0.75,
        "eta": 0.125,
        "a_half": 40.0,
        "phi_age": 0.3,
        "w_half": 4.0,
        "phi_weight": 0.4,
        "mu": 0.4,
        "gamma": 0.8,
        "zeta": 3.5,
        "xi": 1.1,
        "omega": 0.8,
        "F": 50.0,
        "DeltaPhiMax": 10.0
    }

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)

    def eats(self, herbivore):

        if herbivore.fitness > self.fitness:
            return False
        if 0 < self.fitness - herbivore.fitness < self.params['DeltaPhiMax']:
            if random.random() < (
                        (self.fitness - herbivore.fitness) / self.params['DeltaPhiMax']):
                if herbivore.weight >= self.params['F']:
                    self.weight += self.params['F'] * self.params['beta']
                else:
                    self.weight += herbivore.weight * self.params['beta']

            else:
                return True
