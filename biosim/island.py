# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import textwrap
import numpy as np

np.random.seed(1)
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
        self.num_herbivores = []
        self.num_carnivores = []

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

    def set_population_in_cell(self):
        for animal in self.initial_pop:
            location = animal['loc']
            # cell_type = self.island_map[location]
            # if cell_type not in self.valid_landscapes.keys():
            #     raise NameError(f'Location {location} is not a valid location')
            population = animal['pop']
            self.island_map[location].set_population(population)

    def create_island_map(self):
        for y_loc, lines in enumerate(self.island_lines):
            for x_loc, cell_type in enumerate(lines):
                self.island_map[(1 + x_loc, 1 + y_loc)] = self.valid_landscapes[cell_type]()

    def nr_animals_pr_species(self):
        """Create function returning the total nr of herbivores and carnivores in a dict."""
        for y_loc, lines in enumerate(self.island_map):
            for x_loc in enumerate(lines):
                self.num_herbivores.append(len(self.island_map[(x_loc, y_loc)].herbivore_list))
                self.num_carnivores.append(len(self.island_map[(x_loc, y_loc)].carnivore_list))
        return {"Herbivore": sum(self.num_herbivores),
                "Carnivore": sum(self.num_carnivores)}

    def nr_animals(self):
        """Create function which returns total nr of animals on island."""
        total_pop = sum(self.num_herbivores) + sum(self.num_carnivores)
        return total_pop

    def next_cell(self, cell):

        y_cord, x_cord = cell
        loc_1 = (y_cord - 1, x_cord)
        loc_2 = (y_cord + 1, x_cord)
        loc_3 = (y_cord, x_cord - 1)
        loc_4 = (y_cord, x_cord + 1)
        option_1 = self.island_map[loc_1]
        option_2 = self.island_map[loc_2]
        option_3 = self.island_map[loc_3]
        option_4 = self.island_map[loc_4]

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



        # for row, map_object in enumerate(self.island_map):
        #     for col, cell in enumerate(map_object):
        #         if self.island_map[(row, col)].passable is not True:
        #             break
        #         else:
        #             self.cells_probability(cell)

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

        for cell in self.island_map:
            self.island_map[cell].reset_migrate()


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
