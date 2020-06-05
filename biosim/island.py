# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

from biosim.landscapes import Landscape


class Island:

    valid_landscape = ['W', 'D', 'L', 'H']
    initial_pop = [{'loc': (1, 1), 'pop':[{'species':'Herbivore', 'age':1, 'weight': 10.}]}]
    default_island_map = "L"

    def __init__(self, island_map=default_island_map, ini_pop=None):
        self.island_map = island_map
        if ini_pop is None:
            self.initial_pop = Island.initial_pop
        else:
            self.initial_pop = ini_pop

        self.env = Landscape()
        self.env.population['Herbivore'].append(ini_pop)


if __name__ == '__main__':
    island = Island()
    print(island.env.population)


