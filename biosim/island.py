# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

from biosim.landscapes import Landscape


class Island:
    valid_landscape = ['W', 'D', 'L', 'H']
    initial_pop = [{'species': 'Herbivore', 'age': 1, 'weight': 10.},
                   {'species': 'Herbivore', 'age': 3, 'weight': 14.},
                   {'species': 'Herbivore', 'age': 3, 'weight': 14.},
                   {'species': 'Herbivore', 'age': 3, 'weight': 14.},
                   {'species': 'Herbivore', 'age': 3, 'weight': 14.}]
    default_island_map = "L"
    years = 20

    def __init__(self, island_map=default_island_map, ini_pop=None):
        self.island_map = island_map
        if ini_pop is None:
            self.initial_pop = Island.initial_pop
        else:
            self.initial_pop = ini_pop

        self.env = Landscape()
        self.env.set_population(self.initial_pop)

        year = 0
        while year < Island.years:
            self.env.f_max = 800
            self.env.food_grows()
            self.env.animals_eat()
            self.env.animals_reproduce()
            self.env.animals_age()
            self.env.animals_lose_weight()
            self.env.animals_die()
            year += 1


if __name__ == '__main__':
    island = Island()
    print(island.env.herb_list[0].weight)
    print(island.env.available_food)
    print(island.env.animal_list[0].weight)
    print(len(island.env.animal_list))

