# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import textwrap
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd
import numpy as np
import seaborn as sns
from biosim import island


class Visualization:

    def __init__(self):
        self.dataframe = None
        self.herb_density = None

    def animal_distribution(self, island_map):
        """
        Pandas DataFrame with animal count per species for
        each cell on island.
        :return: pd dataframe: 'rows' 'columns' 'Herbivores' 'Carnivores'
        """
        data = {}
        rows = []
        col = []
        herbs = []
        carns = []
        for coord, cell in island_map.items():
            herbs.append(len(cell.herbivore_list))
            carns.append(len(cell.carnivore_list))
            rows.append(coord[0])
            col.append(coord[1])
        data['Row'] = rows
        data['Col'] = col
        data['Herbivore'] = herbs
        data['Carnivore'] = carns
        self.dataframe = pd.DataFrame(data)

    @staticmethod
    def standard_map(default_geography):
        island_string = default_geography
        string_map = textwrap.dedent(island_string)
        string_map.replace('\n', ' ')

        color_code = {'W': colors.to_rgb('blue'),
                      'L': colors.to_rgb('darkgreen'),
                      'H': colors.to_rgb('lightgreen'),
                      'D': colors.to_rgb('lightyellow')}

        island_map = [[color_code[column] for column in row]
                      for row in string_map.splitlines()]

        fig = plt.figure()
        ax_map = fig.add_subplot(221)
        ax_map.imshow(island_map, interpolation='nearest')
        ax_map.set_title('Geography')
        axlg = fig.add_axes([0.03, 0.525, 0.1, 0.4])
        axlg.axis('off')
        for ix, name in enumerate(('W', 'L', 'H',
                                   'D')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=color_code[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

    def heat_map_herbivore(self):
        """
        Creates heat map plot of carnivores on the island
        """
        herb_cell = self.dataframe.pivot('Row', 'Col', 'Herbivore')
        fig = plt.figure()

        ax_heat_h = fig.add_subplot(224)

        ax_heat_h.imshow(herb_cell,
                         vmax=100,
                         interpolation='nearest',
                         cmap='Greens')

        ax_heat_h.set_title('Herbivore population density')

    def heat_map_carnivore(self):
        """
        Creates heat map plot of carnivores on the island
        """
        carn_cell = self.dataframe.pivot('Row', 'Col', 'Carnivore')

        fig = plt.figure()
        ax_heat_c = fig.add_subplot(224)

        ax_heat_c.imshow(carn_cell,
                         vmax=75,
                         interpolation='nearest',
                         cmap='Reds')
        ax_heat_c.set_title('Carnivore population density')

    def update_all(self):
        """
        Updates plots for simulation
        """
        self.heat_map_carnivore()
        self.heat_map_herbivore()


if __name__ == '__main__':
    pass
