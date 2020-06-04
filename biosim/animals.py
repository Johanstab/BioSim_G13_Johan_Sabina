# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

import numpy as np
import random as random


class Animals:
    default_params = {
        'w_birth': 8.,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40.,
        'phi_age': 0.2,
        'w_half': 10.,
        'phi_weight': 0.1,
        'mu': 0.25,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10.}

    def __init__(self, params=None, age=0, weight=10.):
        if params is not None:
            self.p = params
        else:
            self.p = Animals.default_params

        self.age = age
        self.weight = weight
        self.phi = 0

    def aging(self):
        self.age += 1

    def weight(self, delta_w):
        self.weight += delta_w

    @staticmethod
    def q(sgn, x, x_half, phi):
        return 1. / (1. + np.exp(sgn * phi * (x - x_half)))

    def fitness(self):
        if self.weight <= 0:
            self.phi = 0
        else:
            self.phi = Animals.q(+1, self.age, self.p['a_half'], self.p['phi_age']) * \
                       Animals.q(-1, self.weight, self.p['w_half'], self.p['phi_weight'])
            "Must be 0<Phi<1"

    def death(self):
        if self.weight == 0:
            return True
        elif self.weight * (1 - self.phi) <= 0:
            return True
        else:
            return False


class Herbivore(Animals):
    def __init__(self):
        super(self, Herbivore).__init__()


class Carnivore(Animals):
    def __init__(self):
        super(self, Carnivore).__init__()
