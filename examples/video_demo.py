# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

"""This is a small script that test if the move_maker function in BioSim simulation works"""

from biosim.simulation import BioSim

DEFAULT_IMAGE_BASE = r'/Users/sabinal/Documents/INF200 JUNI/Bilder og videoer/bio'

sim = BioSim(ymax_animals=2000,
             cmax_animals={'Herbivore': 150, 'Carnivore': 80},
             img_base=DEFAULT_IMAGE_BASE)
sim.simulate(25, 1, 1)
sim.make_movie()