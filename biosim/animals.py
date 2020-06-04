# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

import numpy as np
import random as random


class Animals:
    "Move params to different species and create a set_params method"

    @classmethod
    def set_params(cls, new_params):

        for key in new_params:
            if key not in ('w_birth', 'sigma_birth', 'beta', 'eta',
                           'a_half', 'phi_age','w_half', 'phi_weight',
                           'mu', 'gamma', 'zeta', 'xi', 'omega', 'F', 'DeltaPhiMax'
                           ):
                raise KeyError('Invalid parameter name: ' + key)

        if 'eta' in new_params:
            if not new_params['eta'] <= 1:
                raise ValueError('eta must be <= 1.')
            cls.eta = new_params['eta']

        if 'DeltaPhiMax' in new_params:
            if not 0 < new_params['DeltaPhiMax']:
                raise ValueError('DeltaPhiMax must be positive!')
            cls.p_divide = new_params['p_divide']

        pass

    def __init__(self, age=0, weight=None):
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
        prob_death = self.weight * (1 - self.phi)

        if self.weight == 0 or random.random() < prob_death:
            return True
        else:
            return False


class Herbivore(Animals):
    def __init__(self, age, weight):
        super().__init__(age, weight)

        default_params_herbivore = {
            'w_birth': 8.,
            'sigma_birth': 1.5,
            'beta': 0.9,
            'eta': 0.05,
            'a_half': 40.0,
            'phi_age': 0.6,
            'w_half': 10.0,
            'phi_weight': 0.1,
            'mu': 0.25,
            'gamma': 0.2,
            'zeta': 3.5,
            'xi': 1.2,
            'omega': 0.4,
            'F': 10.0,
            'DeltaPhiMax': None}


class Carnivore(Animals):
    def __init__(self, age, weight):
        super().__init__(age, weight)
