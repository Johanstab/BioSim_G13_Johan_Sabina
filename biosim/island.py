# -*- coding: utf-8 -*-

"""
mod: 'biosim.island' provides the user with the annual cycle on Rossumøya.

This script provide the annual cycle of events that accrue on Rossumøya ever year. The island of
Rossumøya is also made in this script.

This file can be imported as a module and contains the following classes:

    * Island - Superclass that contains the ways of making the map of Rossumøya and setting its
     population. It also contains the function that makes the annual cycle of Rossumøya.

Notes
-----
    To run this script, its required to have both 'numpy' and  'matplotlib.pyplot' installed in
    the Python environment that your going to run this script in.

"""

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import textwrap
import numpy as np

import matplotlib.pyplot as plt
from biosim.landscapes import Water, Lowland, Highland, Desert


class Island:
    valid_landscapes = {'W': Water,
                        'D': Desert,
                        'L': Lowland,
                        'H': Highland}

    def __init__(self, island_map=None, ini_pop=None):
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

        top_row = len(self.island_lines[0])
        for lines in self.island_lines:
            if len(lines) is not top_row:
                raise ValueError('Each row in the multiline string should be equal in length')

        for index in range(len(self.island_lines[0])):
            if self.island_lines[0][index] != 'W' or self.island_lines[-1][index] != 'W':
                raise ValueError('This island is out out boundary. Islands should be '
                                 'surrounded by water')

        for index in range(len(self.island_lines)):
            if self.island_lines[index][0] != 'W' or self.island_lines[index][-1] !='W':
                raise ValueError('This island is out out boundary. Islands should be '
                                 'surrounded by water')

        if ini_pop is None:
            self.initial_pop = self.initial_pop
        else:
            self.initial_pop = ini_pop

    def set_population_in_cell(self, new_pop=None):
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
        for cell in self.island_map:
            self.island_map[cell].reset_migrate()

    def cycle_island(self):
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


if __name__ == "__main__":
    island = Island()

    # print(map_.keys())
    # for x in range(1, 5):
    #     for y in range(1, 5):
    #         print(map_[(y, x)])

    print(len(island.island_map[(2, 2)].herbivore_list))
    print(len(island.island_map[(2, 2)].carnivore_list))
    island.island_map[(2, 2)].herbivore_list.sort(key=lambda animal: animal.age, reverse=True)
    print(island.island_map[(2, 2)].herbivore_list[0].age)
    island.island_map[(2, 2)].carnivore_list.sort(key=lambda animal: animal.age, reverse=True)
    print(island.island_map[(2, 2)].carnivore_list[0].age)

    plt.plot(island.num_herbivores, 'b')
    plt.plot(island.num_carnivores, 'r')
    plt.show()
