# -*- coding: utf-8 -*-

"""
mod: 'biosim.island' provides the user with the annual cycle on Rossumøya.

This script provide the annual cycle of events that accrue on Rossumøya ever year. The island of
Rossumøya is also made in this script.

This file can be imported as a module and contains the following class:

    * Island - Class that contains the ways of making the map of Rossumøya and setting its
     population. It also contains the function that makes the annual cycle of Rossumøya.

Notes
-----
    To run this script, its required to have 'numpy', 'matplotlib.pyplot' and 'textwrap' installed
    in the Python environment that your going to run this script in.
"""

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import numpy as np
import textwrap

from biosim.landscapes import Water, Lowland, Highland, Desert


class Island:
    """Class for Island in Biosim"""

    valid_landscapes = {'W': Water,
                        'D': Desert,
                        'L': Lowland,
                        'H': Highland}

    def __init__(self, island_map=None, ini_pop=None):
        """Constructor that initiates Island class instances.

        Parameters
        ----------
        island_map: str
                Multiline string indicating geography of the island

        ini_pop: list
                List of dictionaries indicating initial population and location
        """
        self.geography = textwrap.dedent(island_map)
        self.island_lines = self.geography.splitlines()
        self.island_map = {}
        self.create_island_map()
        self.set_population_in_cell(ini_pop)
        self.num_herbivores = []
        self.num_carnivores = []

        for lines in self.island_lines:
            for cell_type in lines:
                if cell_type not in self.valid_landscapes.keys():
                    raise ValueError(f'Cell type {cell_type} does not exist')

        row = len(self.island_lines[0])
        for lines in self.island_lines:
            if len(lines) is not row:
                raise ValueError('Each row in the multiline string should be equal in length')

        for index in range(len(self.island_lines[0])):
            if self.island_lines[0][index] != 'W' or self.island_lines[-1][index] != 'W':
                raise ValueError('This island is out out boundary. Islands should be '
                                 'surrounded by water')

        for index in range(len(self.island_lines)):
            if self.island_lines[index][0] != 'W' or self.island_lines[index][-1] != 'W':
                raise ValueError('This island is out out boundary. Islands should be '
                                 'surrounded by water')

        if ini_pop is None:
            self.initial_pop = self.initial_pop
        else:
            self.initial_pop = ini_pop

    def set_population_in_cell(self, new_pop=None):
        """Makes it possible to put out a 'new' set of population in any cell on the island

        Parameters
        ----------
        new_pop: list
                List of dicts that contains the new population that you want to place in the current
                cell
        """
        if new_pop is None:
            init_pop = self.initial_pop
        else:
            init_pop = new_pop

        for animal in init_pop:
            location = animal['loc']
            if location not in self.island_map.keys():
                raise ValueError(f'Location {location} is not a valid location.')
            elif self.island_map[location].passable is False:
                raise ValueError(
                    f'Location {self.island_map[location]} is not habitable landscape.')
            population = animal['pop']
            self.island_map[location].set_population(population)

    def create_island_map(self):
        """Creates the island map form the given geography"""
        for y_loc, lines in enumerate(self.island_lines):
            for x_loc, cell_type in enumerate(lines):
                if cell_type not in self.valid_landscapes.keys():
                    raise ValueError(f'Cell type: {cell_type} is not valid')
                self.island_map[(1 + y_loc, 1 + x_loc)] = self.valid_landscapes[cell_type]()
        return self.island_map

    def nr_animals_pr_species(self):
        """Create function returning the total nr of herbivores and carnivores in a dict."""
        nr_herbs = 0
        nr_carns = 0
        for cell in self.island_map:
            if self.island_map[cell].passable:
                nr_herbs += len(self.island_map[cell].herbivore_list)
                nr_carns += len(self.island_map[cell].carnivore_list)

        nr_animals = {'Herbivore': nr_herbs, 'Carnivore': nr_carns}
        return nr_animals

    def nr_animals(self):
        """Create function which returns total nr of animals on island."""
        total_species = self.nr_animals_pr_species()
        total_pop = total_species['Herbivore'] + total_species['Carnivore']
        return total_pop

    @staticmethod
    def next_cell(cell):
        """Finds the neighboring cells of the cell were the animal want to move from.

        Parameters
        ----------
        cell: tuple
             The position/coordinates of the current landscape cell.
        """
        y_cord, x_cord = cell
        loc_1 = (y_cord - 1, x_cord)
        loc_2 = (y_cord + 1, x_cord)
        loc_3 = (y_cord, x_cord - 1)
        loc_4 = (y_cord, x_cord + 1)

        list_ = [loc_1, loc_2,
                 loc_3, loc_4]

        chosen_cell = np.random.choice(len(list_))
        chosen_cell = list_[chosen_cell]

        return chosen_cell

    def migrate_animals(self, cell):
        """Checks if the cell in question have animals in it (if it passable). Makes a list of all
        animals i the current cell that wants to move, and checks if the cell that the animals want
        to move to is passable. Places the animal in its new cell and removes it for the old one.

        Parameters
        ----------
        cell: object
            The current landscape cell that the animal i positioned in.
        """
        if self.island_map[cell].passable:
            herb_move, carn_move = self.island_map[cell].animals_migrate()
            for herb in herb_move:
                new_loc = self.next_cell(cell)
                if not self.island_map[new_loc].passable:
                    break
                else:
                    self.island_map[new_loc].add_population(herb)
                    herb.has_moved = True
                    self.island_map[cell].herbivore_list.remove(herb)
            for carn in carn_move:
                new_loc = self.next_cell(cell)
                if not self.island_map[new_loc].passable:
                    break
                else:
                    self.island_map[new_loc].add_population(carn)
                    carn.has_moved = True
                    self.island_map[cell].carnivore_list.remove(carn)

    def reset_migration(self):
        """Resets if the animal has moved or not, so the value can be updated each year."""
        for cell in self.island_map:
            self.island_map[cell].reset_migrate()

    def cycle_island(self):
        """Simulates annual cycle of Rossumøya for all the cells the island i made out of."""
        for cell in self.island_map:
            self.island_map[cell].food_grows()
            self.island_map[cell].herbivore_eats()
            self.island_map[cell].carnivore_eats()
            self.island_map[cell].herbivore_reproduce()
            self.island_map[cell].carnivore_reproduce()
            self.migrate_animals(cell)
            self.island_map[cell].animals_age()
            self.island_map[cell].animals_lose_weight()
            self.island_map[cell].animals_die()

        self.reset_migration()

    @property
    def fitness_age_weight(self):
        list1_herb = []
        list1_carn = []
        list2_herb = []
        list2_carn = []
        list3_herb = []
        list3_carn = []
        plot_attributes_herb = {'fitness': [],
                           'age': [],
                           'weight': []}
        plot_attributes_carn = {'fitness': [],
                                'age': [],
                                'weight': []}
        for cell in self.island_map:
            if self.island_map[cell].passable:
                for animal in self.island_map[cell].herbivore_list:
                    list1_herb.append(animal.fitness)
                    list2_herb.append(animal.age)
                    list3_herb.append(animal.weight)

                for animal in self.island_map[cell].carnivore_list:
                    list1_carn.append(animal.fitness)
                    list2_carn.append(animal.age)
                    list3_carn.append(animal.weight)
        plot_attributes_herb['fitness'] = np.array(list1_herb)
        plot_attributes_herb['age'] = np.array(list2_herb)
        plot_attributes_herb['weight'] = np.array(list3_herb)

        plot_attributes_carn['fitness'] = np.array(list1_carn)
        plot_attributes_carn['age'] = np.array(list2_carn)
        plot_attributes_carn['weight'] = np.array(list3_carn)
        return plot_attributes_herb, plot_attributes_carn
