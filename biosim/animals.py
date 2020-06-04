# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'


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

    def __init__(self, params=default_params):
        pass


class Herbivore(Animals):
    def __init__(self):
        pass


class Carnivore(Animals):
    def __init__(self):
        pass
