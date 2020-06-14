# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import numpy as np
import matplotlib.pyplot as plt
from biosim.island import Island
from biosim.visualization import Visualization


class BioSim:
    initial_pop = [
        {'loc': (2, 2),
         'pop':
             [{'species': 'Carnivore', 'age': 5, 'weight': 20.0} for _ in range(20)]},
        {'loc': (2, 2),
         'pop':
             [{'species': 'Herbivore', 'age': 5, 'weight': 20.0} for _ in range(50)]}
    ]

    default_geography = """\
                        WWWW
                        WLLW
                        WLLW
                        WWWW"""

    def __init__(
            self,
            island_map=None,
            ini_pop=None,
            seed=1,
            ymax_animals=None,
            cmax_animals=None,
            hist_specs=None,
            img_base=None,
            img_fmt="png",
    ):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population
        :param seed: Integer used as random number seed
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param img_base: String with beginning of file name for figures, including path
        :param img_fmt: String with file type for figures, e.g. 'png'
        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
        {'Herbivore': 50, 'Carnivore': 20}
        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,
        {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}
        Permitted properties are 'weight', 'age', 'fitness'.
        If img_base is None, no figures are written to file.
        Filenames are formed as
        '{}_{:05d}.{}'.format(img_base, img_no, img_fmt)
        where img_no are consecutive image numbers starting from 0.
        img_base should contain a path and beginning of a file name.
        """
        self.island = None
        self.num_images = 0
        self.current_year = 0
        self.seed = seed
        self.ini_pop = self.initial_pop
        self.island_map = self.default_geography
        self.ymax_animals = ymax_animals
        self.img_fmt = img_fmt
        self.img_base = img_base
        self.cmax_animals = cmax_animals

        if self.cmax_animals is None:
            self.cmax_animals = {'Herbivore': 150, 'Carnivore': 90}

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.
        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species
        """

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.
        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape
        """

    def simulate(self, num_years, vis_years=1, img_years=None):
        """
        Run simulation while visualizing the result.
        :param num_years: number of years to simulate
        :param vis_years: years between visualization updates
        :param img_years: years between visualizations saved to files (default: vis_years)
        Image files will be numbered consecutively.
        """
        self.island = Island(self.island_map, self.ini_pop)
        vis = Visualization()
        vis.set_graphics(self.ymax_animals, num_years)
        vis.standard_map(self.island_map)
        self.island.create_island_map()
        self.island.set_population_in_cell()

        while self.current_year < num_years:
            if self.current_year == 50:
                input('Press enter to continue....')
                self.island.set_population_in_cell()
            self.island.cycle_island()
            self.current_year += 1

        # vis.animal_distribution(island.island_map)
        # vis.update_herb_ax(200)
        # vis.update_carn_ax(100)
        # vis.update_mean_ax()
        # plt.show()

    def add_population(self, population):
        """
        Add a population to the island
        :param population: List of dictionaries specifying population
        """

    @property
    def year(self):
        """Last year simulated."""
        return self.current_year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.island.nr_animals()

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return self.island.nr_animals_pr_species()

    def make_movie(self):
        """Create MPEG4 movie from visualization images saved."""


if __name__ == '__main__':
    BioSim = BioSim()
    BioSim.simulate(200)
    print(BioSim.num_animals)
    print(BioSim.num_animals_per_species)


