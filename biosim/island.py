# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import textwrap
import numpy as np
np.random.seed(1)
from biosim.landscapes import Water, Lowland, Highland, Desert


class Island:
    valid_landscapes = {"W": Water,
                        "D": Desert,
                        "L": Lowland,
                        "H": Highland}
    initial_pop = [
        {'loc': (2, 2),
         'pop':
             [{"species": "Carnivore", "age": 5, "weight": 20.0} for _ in range(20)]},
        {'loc': (2, 2),
         'pop':
             [{"species": "Herbivore", "age": 5, "weight": 20.0} for _ in range(50)]}
    ]
    default_geogr = """\
                        WWWW
                        WLLW
                        WLLW
                        WWWW"""
    default_geogr = textwrap.dedent(default_geogr)
    years = 100

    def __init__(self, island_map=default_geogr, ini_pop=None, sim_years=years, seed=1):
        self.default_geogr = textwrap.dedent(island_map)
        self.island_lines = self.default_geogr.splitlines()
        self.island_map = {}
        np.random.seed(1)

        for lines in self.island_lines:
            for cell_type in lines:
                if cell_type not in self.valid_landscapes.keys():
                    raise NameError(f'Cell type {cell_type} does not exist')

        top_row = len(self.island_lines[0])
        for lines in self.island_lines:
            if len(lines) is not top_row:
                raise ValueError('Each row in the multiline string should be equal in length')

        if ini_pop is None:
            self.initial_pop = self.initial_pop
        else:
            self.initial_pop = ini_pop

        self.years = sim_years
        self.create_island_map()
        self.set_population_in_cell()

        year = 0
        while year < Island.years:
            self.island_map[(2, 2)].food_grows()
            self.island_map[(2, 2)].herbivore_eats()
            self.island_map[(2, 2)].carnivore_eats()
            self.island_map[(2, 2)].herbivore_reproduce()
            self.island_map[(2, 2)].carnivore_reproduce()
            self.island_map[(2, 2)].animals_age()
            self.island_map[(2, 2)].animals_lose_weight()
            self.island_map[(2, 2)].animals_die()
            year += 1

    def set_population_in_cell(self):
        for animal_loc in self.initial_pop:
            location = animal_loc['loc']
            cell_type = self.island_map[location]
            # if cell_type not in self.valid_landscapes.keys():
            #     raise NameError(f'Location {location} is not a valid location')
            population = animal_loc['pop']
            self.island_map[location].set_population(population)

    def create_island_map(self):
        for y_loc, lines in enumerate(self.island_lines):
            for x_loc, cell_type in enumerate(lines):
                self.island_map[(1 + x_loc, 1 + y_loc)] = self.valid_landscapes[cell_type]()


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


