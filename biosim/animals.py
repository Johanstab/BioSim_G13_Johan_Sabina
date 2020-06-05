# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

import numpy as np
import random as random


class Animals:
    "Move params to different species and create a set_params method"
    keys = ['w_birth', 'sigma_birth', 'beta', 'eta',
            'a_half', 'phi_age', 'w_half', 'phi_weight',
            'mu', 'gamma', 'zeta', 'xi', 'omega', 'F', 'DeltaPhiMax']
    params = dict.fromkeys(keys)

    @classmethod
    def set_params(cls, new_params):
        for key in new_params:
            if key not in Animals.keys:
                raise KeyError('Invalid parameter name: ' + key)

        for iterator in new_params:
            if iterator == 'eta' and new_params[iterator] >= 1:
                raise ValueError('eta must be <= 1.')
            if iterator == 'DeltaPhiMax' and new_params[iterator] <= 0:
                raise ValueError('DeltaPhiMax must be positive!')
            if new_params[iterator] < 0:
                raise ValueError('{} cannot be negative'.format(iterator))
            cls.params[iterator] = new_params[iterator]

    def __init__(self, age=0, weight=None):
        self.age = age
        self.weight = weight
        self.phi = 0

        if self.weight is None:
            self.weight = self.weight_birth(self.params['w_birth'], self.params['sigma_birth'])

    @staticmethod
    def weight_birth(weight, sigma):
        return np.random.normal(weight, sigma)

    def age(self):
        return self.age

    def aging(self):
        self.age += 1

    def weight_gain(self):
        self.weight += self.params['F'] * self.params['beta']
        return self.weight

    def weight_loss(self):
        self.weight -= self.params['eta'] * self.weight
        return self.weight

    @staticmethod
    def q(sgn, x, x_half, phi):
        return 1. / (1. + np.exp(sgn * phi * (x - x_half)))

    @property
    def fitness(self):
        if self.weight <= 0:
            self.phi = 0
        else:
            self.phi = Animals.q(+1, self.age, self.params['a_half'], self.params['phi_age']) * \
                       Animals.q(-1, self.weight, self.params['w_half'], self.params['phi_weight'])
        return self.phi

    def birth(self, nr_animals):
        b_prob = min(1, self.params['gamma'] *
                     self.fitness * (nr_animals - 1))
        if nr_animals < 2:
            return False
        if self.weight < self.params['zeta'] * (
                self.params['w_birth'] + self.params['sigma_birth']):
            return False
        return random.random() < b_prob

    @property
    def death_probability(self):
        if self.weight == 0:
            return False

        prob_death = self.weight * (1 - self.phi)
        return random.random() < prob_death


class Herbivore(Animals):
    params = {'w_birth': 8.,
              'sigma_birth': 1.5,
              'beta': 0.9,
              'eta': 0.05,
              'a_half': 40.,
              'phi_age': 0.6,
              'w_half': 10.,
              'phi_weight': 0.1,
              'mu': 0.25,
              'gamma': 0.2,
              'zeta': 3.5,
              'xi': 1.2,
              'omega': 0.4,
              'F': 10.}

    def __init__(self, age=0, weight=None):

        super().__init__(age, weight)

    def eats(self, cell):
        if self.params['F'] <= cell.availabe_fodder:
            self.weight = self.weight_gain()
        else:
            self.weight = self.params['beta']*cell.availabe_fodder


class Carnivore(Animals):
    def __init__(self, age, weight):
        super().__init__(age, weight)
