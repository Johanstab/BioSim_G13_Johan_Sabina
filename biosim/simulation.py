# -*- coding: utf-8 -*-

"""
:mod: 'biosim.simulation' provides the user with the interface to the package.

This file wil run the simulation of island. The simulation will run for a given amount of years.
This file will use the visualization file, to provide visualization of the simulation.

The visualization is given in one graphics window with the following elements:

    *   A map of geography of the island. It' is shows different colors for the different
        landscape types.
    *   Line graph that shows the total number of animals in the island by
        species.
    *   Distribution heat maps with color bars that shows how many animals per species
        there are in each cell of the island

This file can be imported as a module and contains the following
class:

    *   BioSim - Simulation interface module

Notes
-----
    To run this script, its required to have 'numpy', 'pandas', 'matplotlib.pyplot', 'os' and
    'subprocess' installed in the Python environment that your going to run this script in. It also
    requires 'ffmpeg' to run the movie_maker function.
"""

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from biosim.island import Island
from biosim.visualization import Visualization
from biosim.animals import Herbivore, Carnivore
from biosim.landscapes import Lowland, Highland

import os
import subprocess


# update these variables to point to your ffmpeg and convert binaries
_FFMPEG_BINARY = "ffmpeg"
_CONVERT_BINARY = "magick"

# update this to the directory and file-name beginning for the graphics files
_DEFAULT_GRAPHICS_DIR = os.path.join("..", "figs")
_DEFAULT_IMAGE_NAME = "bio"
_DEFAULT_IMAGE_FORMAT = "png"
_DEFAULT_MOVIE_FORMAT = "mp4"
DEFAULT_IMAGE_BASE = os.path.join(_DEFAULT_GRAPHICS_DIR, _DEFAULT_IMAGE_NAME)


class BioSim:
    """Simulation interface class."""

    default_pop = [
        {
            "loc": (4, 4),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20.0} for _ in range(20)],
        },
        {
            "loc": (4, 4),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20.0} for _ in range(50)],
        },
    ]

    default_geography = """\
                            WWWWWWWWWWWWWWWWWWWWW
                            WWWWWWWWHWWWWLLLLLLLW
                            WHHHHHLLLLWWLLLWWLLWW
                            WHHHHHHHWHWWLLLLLLWWW
                            WHHHHLLLLLLWLLLLLLWWW
                            WHHHHLLLLDDLLLHLLLWWW
                            WHHLLLLLDDDLLLHHHHWWW
                            WWHHHHLLLDDLLLHWWWWWW
                            WHHHLLLLLDDLLLLLLLWWW
                            WHHHHLLLLDDLLLLWWWWWW
                            WWHHHHLLLLLLLLWWWWWWW
                            WWWHHHHLLLLLLLWWWWWWW
                            WWWWWWWWWWWWWWWWWWWWW"""

    def __init__(
        self,
        island_map=None,
        ini_pop=None,
        seed=1,
        ymax_animals=None,
        cmax_animals=None,
        hist_specs=None,
        img_base=None,
        img_fmt=None,
    ):
        """
        Parameters
        ----------
        island_map : str
                Multi-line string specifying island geography

        ini_pop : list
                List of dictionaries specifying initial population

        seed : int
                 Integer used as random number seed

        ymax_animals : int
                Number specifying y-axis limit for graph showing animal numbers

        cmax_animals : dict
                 Dict specifying color-code limits for animal densities

        hist_specs :
                Specifications for histograms, see below

        img_base : str
                String with beginning of file name for figures, including path

        img_fmt : str
                String with file type for figures, e.g. 'png'

        If ymax_animals is None, the y-axis limit should be adjusted automatically.

        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,
        {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g., {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}

        If img_base is None, no figures are written to file. Filenames are formed as '{}_{:05d}.{}'
        .format(img_base, img_no, img_fmt) where img_no are consecutive image numbers starting from
        0. img_base should contain a path and beginning of a file name.
        """
        np.random.seed(seed)

        if ini_pop is None:
            self.ini_pop = self.default_pop
        else:
            self.ini_pop = ini_pop

        if island_map is None:
            self.island_map = self.default_geography
        else:
            self.island_map = island_map

        if hist_specs is None:
            self.hist_specs = {
                "weight": {"max": 60, "delta": 2},
                "fitness": {"max": 1.0, "delta": 0.05},
                "age": {"max": 60, "delta": 2},
            }
        else:
            self.hist_specs = hist_specs

        self.island = Island(self.island_map, self.ini_pop)
        self.num_images = 0
        self._current_year = 0
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals
        self._image_counter = 0
        self._count = 0

        if self.ymax_animals is None:
            self.ymax_animals = 20000

        if self.cmax_animals is None:
            self.cmax_animals = {"Herbivore": 150, "Carnivore": 90}

        if img_base is not None:
            self._image_base = img_base
        else:
            self._image_base = None

        if img_fmt is None:
            img_fmt = _DEFAULT_IMAGE_FORMAT
        self._image_format = img_fmt

        self._image_counter = 0
        self.vis = Visualization(self.cmax_animals, self.hist_specs)

    @staticmethod
    def set_animal_parameters(species, params):
        """Set parameters for animal species.

        Parameters
        ----------
        species : str
               String, name of animal species

        params : dict
               Dict with valid parameter specification for species
        """
        if species == "Herbivore":
            Herbivore.set_params(params)
        elif species == "Carnivore":
            Carnivore.set_params(params)

    @staticmethod
    def set_landscape_parameters(landscape, params):
        """Set parameters for landscape type.

        Parameters
        ----------
        landscape : str
                 String, code letter for landscape

        params : dict
                Dict with valid parameter specification for landscape
        """
        if landscape == "Lowland":
            Lowland.set_params(params)
        elif landscape == "Highland":
            Highland.set_params(params)

    def simulate(self, num_years, vis_years=1, img_years=None):
        """Run simulation while visualizing the result.

        Parameters
        ----------
        num_years : int
                Number of years to simulate
        vis_years : int
                Years between visualization updates
        img_years : int
                Years between visualizations saved to files (default: vis_years)

        Image files will be numbered consecutively.
        """
        num_years = self._current_year + num_years
        self.vis.set_graphics(self.ymax_animals, num_years + 1, self.year)
        self.vis.standard_map(self.island_map)
        self.vis.update_herb_heatmap(self.animal_distribution)
        self.vis.update_carn_heatmap(self.animal_distribution)
        self.vis.update_fitness(
            self.island.fitness_age_weight[0], self.island.fitness_age_weight[1]
        )
        self.vis.update_age(self.island.fitness_age_weight[0], self.island.fitness_age_weight[1])
        self.vis.update_weight(self.island.fitness_age_weight[0], self.island.fitness_age_weight[1])

        while self._current_year < num_years:
            self.island.cycle_island()
            self._current_year += 1
            if self._count % vis_years == 0:
                self.vis.update_graphics(
                    self.animal_distribution,
                    self.num_animals_per_species,
                    self.year,
                    self.island.fitness_age_weight[0],
                    self.island.fitness_age_weight[1],
                )

            if self._count % img_years == 0:
                self._save_file()
            self._count += 1

    def add_population(self, population):
        """Add a population to the island

        Parameters
        ----------
        population : list
                List of dictionaries specifying population
        """
        self.island.set_population_in_cell(population)

    @property
    def year(self):
        """Last year simulated."""
        return self._current_year

    @property
    def num_animals(self):
        """Total number of animals on island."""
        return self.island.nr_animals()

    @property
    def num_animals_per_species(self):
        """Number of animals per species in island, as dictionary."""
        return self.island.nr_animals_pr_species()

    @property
    def animal_distribution(self):
        """Makes a dataframe of the animal_distribution on the island, to use in the visualization
        heat maps.

        Returns
        -------
        df
            Dataframe used in heat map visualization

        """
        data = {}
        rows = []
        col = []
        herbs = []
        carns = []
        for coord, cell in self.island.island_map.items():
            herbs.append(len(cell.herbivore_list))
            carns.append(len(cell.carnivore_list))
            rows.append(coord[0])
            col.append(coord[1])
        data["Row"] = rows
        data["Col"] = col
        data["Herbivore"] = herbs
        data["Carnivore"] = carns
        df = pd.DataFrame(data)
        return df

    def _save_file(self):
        """Saves graphics to file if file name given."""

        if self._image_base is None:
            return

        plt.savefig(
            "{base}_{num:05d}.{type}".format(
                base=self._image_base, num=self._image_counter, type=self._image_format
            )
        )
        self._image_counter += 1

    def make_movie(self):
        """This function is based and heavily inspired by Plesser H.E [1]_

        Create MPEG4 movie from visualization images saved."""

        movie_fmt = "mp4"
        if self._image_base is None:
            raise RuntimeError("No filename defined.")

        try:
            subprocess.check_call(
                [
                    _FFMPEG_BINARY,
                    "-i",
                    "{}_%05d.png".format(self._image_base),
                    "-y",
                    "-profile:v",
                    "baseline",
                    "-filter:v",
                    "setpts=5*PTS",
                    "-level",
                    "3.0",
                    "-pix_fmt",
                    "yuv420p",
                    "{}.{}".format(self._image_base, movie_fmt),
                ]
            )

        except subprocess.CalledProcessError as err:
            raise RuntimeError("ERROR: ffmpeg failed with: {}".format(err))

    def save_simulation(self, name):
        """ Saves the state of the island at the time it is called.

            * Set the 'name' for the file.
            * The file gets saved.
            * Use BioSim.load_simulation to load the saved data.

        Parameters
        ----------
        name : str
                The name the file shall have.
        Returns
        -------
            Dumps/saves a pickled file
        """
        with open(name + ".pickle", "wb") as save_file:
            pickle.dump(self.island, save_file, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load_simulation(name):
        """ Loads a already pickled file and returns the content.

            * Input the 'name' of the file that was saved.
            * Set the data equal to some name.
            * Use this name further to replace existing island or place a new.

        For an example check: BioSim_G13_Johan_Sabina\examples\check_sim_pickled.py

        Parameters
        ----------
        name : str
                The name of the file you want to load.
        Returns
        -------
            The state of the pickled object.
        """
        with open(name + ".pickle", "rb") as load_file:
            return pickle.load(load_file)
