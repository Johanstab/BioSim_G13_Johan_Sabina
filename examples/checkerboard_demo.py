# -*- coding: utf-8 -*-

"""
:mod: `BioSim_G13_Johan_Sabina.checkerboard_demo` is a small demo script running a BioSim
       simulation that test if the animals migrate and move the right way. They should move
       according to information and pictures given by the project task
"""

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'


import textwrap
import matplotlib.pyplot as plt

from biosim.simulation import BioSim

DEFAULT_IMAGE_BASE = r'/Users/sabinal/Documents/INF200 JUNI/Bilder og videoer/bio'

if __name__ == "__main__":
    plt.ion()

    geogr = """\
                WWWWWWWWW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WDDDDDDDW
                WWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    ini_population = [
        {
            "loc": (5, 5),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 50} for _ in range(1000)],
        },
        {
            "loc": (5, 5),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 50} for _ in range(1000)],
        }
    ]

    sim = BioSim(
        island_map=geogr,
        ini_pop=ini_population,
        seed=123456,
        hist_specs={
            "fitness": {"max": 1.0, "delta": 0.05},
            "age": {"max": 60.0, "delta": 2},
            "weight": {"max": 60, "delta": 2},
        }, img_base=DEFAULT_IMAGE_BASE
    )

    sim.set_animal_parameters('Herbivore',
                              {'mu': 1, 'omega': 0, 'gamma': 0,
                               'a_half': 1000})
    sim.set_animal_parameters('Carnivore',
                              {'mu': 1, 'omega': 0, 'gamma': 0,
                               'F': 0, 'a_half': 1000})

    sim.simulate(num_years=10, vis_years=1, img_years=1)
    sim.make_movie()
