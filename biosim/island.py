# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

from biosim.landscapes import Landscape, Water, Lowland, Highland, Desert
import textwrap
import random

random.seed(123456)


class Island:
    valid_landscapes = {"W": Water,
                        "D": Desert,
                        "L": Lowland,
                        "H": Highland}
    initial_pop = [
        {'loc': (2, 2),
         'pop':
             [{"species": "Carnivore", "age": 5, "weight": 15.0} for _ in range(50)]},
        {'loc': (2, 2),
         'pop':
             [{"species": "Herbivore", "age": 5, "weight": 20.0} for _ in range(150)]}
    ]
    default_geogr = """\
                        WWWW
                        WLLW
                        WLLW
                        WWWW"""
    default_geogr = textwrap.dedent(default_geogr)
    years = 20

    def __init__(self, island_map=default_geogr, ini_pop=None, sim_years=years):
        self.default_geogr = textwrap.dedent(island_map)
        self.island_lines = self.default_geogr.splitlines()

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

        self.env = Landscape()
        for list_ in self.initial_pop:
            pop = list_['pop']
            self.env.set_population(pop)

        year = 0
        # while year < Island.years:
        #     self.env.f_max = 800
        #     self.env.food_grows()
        #     self.env.herbivore_eats()
        #     self.env.carnivore_eats()
        #     self.env.herbivore_reproduce()
        #     self.env.carnivore_reproduce()
        #     self.env.animals_age()
        #     self.env.animals_lose_weight()
        #     self.env.animals_die()
        #     year += 1

    def create_island_map(self):
        island_map = {}

        for y_loc, lines in enumerate(self.island_lines):
            for x_loc, cell_type in enumerate(lines):
                island_map[(1 + x_loc, 1 + y_loc)] = self.valid_landscapes[cell_type]()
        return island_map


if __name__ == "__main__":
    island = Island()
    map_ = island.create_island_map()
    print(map_.keys())
    for x in range(1, 5):
        for y in range(1, 5):
            print(map_[(y, x)])

    print(len(island.env.herbivore_list))
    print(len(island.env.carnivore_list))
