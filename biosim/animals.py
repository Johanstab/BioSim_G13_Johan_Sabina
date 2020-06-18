# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import numpy as np
from numba import jit


class Animals:
    "Move params to different species and create a set_params method"
    params = {}

    @classmethod
    def set_params(cls, new_params):
        for key in new_params:
            if key not in Animals.params:
                raise KeyError("Invalid parameter name: " + key)

        for iterator in new_params:
            if iterator == "eta" and new_params[iterator] >= 1:
                raise ValueError("eta must be <= 1.")
            if iterator == "DeltaPhiMax" and new_params[iterator] <= 0:
                raise ValueError("DeltaPhiMax must be positive!")
            if new_params[iterator] < 0:
                raise ValueError("{} cannot be negative".format(iterator))
            cls.params.update(iterator)
            # Implementer en metode med dict.update

    def __init__(self, age=0, weight=None):
        self._age = age
        self._weight = weight
        self.phi = 0
        self.prob_death = 0

        if self._weight is None:
            self._weight = self.weight_birth(self.params["w_birth"], self.params["sigma_birth"])

    @staticmethod
    def weight_birth(weight, sigma):
        """ Calculates a birth _weight for the animal class based on Gaussian distribution.

        Parameters
        ----------
        weight : float
                The mean birth weight wanted.
        sigma : float
                The standard weight deviation wanted.
        Returns
        -------
        float
            The birth weight of a new animal.
        """
        return np.random.normal(weight, sigma)

    @staticmethod
    @jit  # Speeds it up at aprox 2 times faster.
    def q(sgn, x, x_half, phi):
        """ Logistical regression using the Sigmoid function. Later used to calculate
         the fitness of animals.

        Parameters
        ----------
        sgn : int
            Sign determining if positive or negative polarity.
        x  : int or float
            The age or weight of the animal.
        x_half  : float
            Parameter defining at which weight/age the fitness shall deteriorate or grow.
        phi  : float
            Defining the

        Returns
        -------
        float
            Value later used to determine fitness.
        """
        return 1.0 / (1.0 + np.exp(sgn * phi * (x - x_half)))

    @property
    def age(self):
        """"Getter for age"""
        return self._age

    @age.setter
    def age(self, new_age):
        self._age = new_age

    @property
    def weight(self):
        """Getter for weight"""
        return self._weight

    @weight.setter
    def weight(self, new_weight):
        self._weight = new_weight

    def aging(self):
        """Function to increase the age of the animal.

        Returns
        -------
        None
        """
        self._age += 1

    def weight_loss(self):
        """ The natural weight loss an animal goes through each year.

        Returns
        -------
        None
        """
        self._weight -= self.params["eta"] * self.weight

    @property
    def fitness(self):
        """ Determines the fitness of an animal based on Sigmoid functions.

        Returns
        -------
        float
            The generated fitness of the animal.
        """
        if self.weight <= 0:
            return 0
        else:
            return self.q(+1, self.age, self.params["a_half"], self.params["phi_age"])\
                   * self.q(-1, self.weight, self.params["w_half"], self.params["phi_weight"])

    def birth(self, nr_animals):
        """ Determines if the animal should reproduce or not. Then updating the weight of the
        parent and producing a new instance of a Herbivore or Carnivore based on which
        species it is.

        Parameters
        ----------
        nr_animals : int
                The number of same sex animals in the cell.
        Returns
        -------
        bool
            Determining if there should be born a baby or not.
        new_baby
             A new Herbivore or Carnivore object.
        """
        if self.weight < self.params["zeta"] * (
                self.params["w_birth"] + self.params["sigma_birth"]):
            return None

        b_prob = min(1, self.params["gamma"] * self.fitness * (nr_animals - 1))

        if np.random.random() < b_prob:
            if type(self) is Herbivore:
                new_baby = Herbivore()
            elif type(self) is Carnivore:
                new_baby = Carnivore()
            else:
                raise TypeError(f'Type {type(self)} is not valid')
            if new_baby.weight * self.params['xi'] < self.weight:
                self._weight -= new_baby.weight * self.params['xi']
                return new_baby
            else:
                return None
        else:
            return None

    def death(self):
        """Decides if an animal shall die or not based on randomness. The fitter an animal is
        the higher chances it has for survival.

        Returns
        -------
        bool
            Determines if the animal shall die or not.
        """
        if self.weight == 0:
            return True

        prob_death = self.params['omega'] * (1 - self.fitness)
        return np.random.random() < prob_death


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
        "DeltaPhiMax": None,
    }

    def __init__(self, age=0, weight=None):
        super().__init__(age, weight)

    def eats(self, cell):
        """Increases weight according to available food and parameters."""
        self._weight += cell * self.params['beta']


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

    def slay(self, herb):
        """Determines by probability and the fitness of both the herbivore and carnivore if
        the carnivore should kill the herbivore.

        Parameters
        ----------
        herb : instance
                An instance of a herbivore object containing all the information of that animal.
        Returns
        -------
        bool
            Should the herbivore be killed or not.
        """
        return np.random.random() < (self.fitness - herb.fitness) / self.params['DeltaPhiMax']

    def eat(self, herb_sorted_least_fit):
        """Defining how much the carnivore should eat based on the weight of the herbivore and
        the amount it has already eaten. Gains weight based set parameters and how much it has
        eaten.


        Parameters
        ----------
        herb_sorted_least_fit : List
                Sorted list containing all the herbivore objects.
        Returns
        -------
        None
        """
        eaten = 0
        list_of_dead = []

        for herb in herb_sorted_least_fit:

            if eaten >= self.params['F']:
                break

            if herb.fitness >= self.fitness:
                break
            elif 0 < self.fitness - herb.fitness < self.params['DeltaPhiMax']:
                if self.slay(herb):
                    list_of_dead.append(herb)
                    if herb.weight + eaten < self.params['F']:
                        eaten += herb.weight
                        self.weight += herb.weight * self.params['beta']
                    else:
                        self.weight += (self.params['F'] - eaten) * self.params['beta']
                        eaten += self.params['F'] - eaten
            else:
                if self.slay(herb):
                    list_of_dead.append(herb)
                    if herb.weight + eaten < self.params['F']:
                        eaten += herb.weight
                        self.weight += herb.weight * self.params['beta']
                    else:
                        self.weight += (self.params['F'] - eaten) * self.params['beta']
                        eaten += self.params['F'] - eaten

        new_updated_list = [animal for animal in herb_sorted_least_fit if
                            animal not in list_of_dead]
        return new_updated_list

