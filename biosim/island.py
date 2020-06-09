# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

from biosim.landscapes import Landscape
import numpy as np

tom_liste = []


class Island:
    valid_landscape = ["W", "D", "L", "H"]
    initial_pop = [
        {"species": "Herbivore", "age": 1, "weight": 10.0},
        {"species": "Herbivore", "age": 3, "weight": 14.0},
        {"species": "Herbivore", "age": 3, "weight": 14.0},
        {"species": "Herbivore", "age": 3, "weight": 14.0},
        {"species": "Herbivore", "age": 3, "weight": 14.0},
    ]
    default_island_map = "L"
    years = 500

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
            #tom_liste.append(self.env.death_list_herbi)
            year += 1

            #print(len(self.env.herbivore_list))


            #print(self.env.available_food)
            # for animal in self.env.herb_list:
            #     print(animal.phi)
            #print(len(self.env.herbivore_list))

            #for _ in self.env.death_list_herbi:
                #print(len(self.env.death_list_herbi))


if __name__ == "__main__":
    island = Island()
    print(island.env.herbivore_list[1].weight)
    print(island.env.available_food)
    #print(island.env.animal_list[0])
    print(len(island.env.herbivore_list))
    summ = 0
    for animal in island.env.herbivore_list:
        summ += animal.age

    mean = summ/len(island.env.herbivore_list)
    print(mean)
    #print(island.env.death_list_herbi)
    #print(len(tom_liste))
