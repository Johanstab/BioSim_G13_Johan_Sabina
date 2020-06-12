# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import textwrap
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd
from biosim import island


class Visualization:

    def animal_distribution(island_map):
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
            herbs.append(cell.herbivore_list)
            carns.append(cell.carnivore_list)
            rows.append(coord[0])
            col.append(coord[1])
        data['Row'] = rows
        data['Col'] = col
        data['Herbivore'] = herbs
        data['Carnivore'] = carns
        return pd.DataFrame(data)

    def standard_map(default_geography):
        island_string = default_geography
        string_map = textwrap.dedent(island_string)
        string_map.replace('\n', ' ')

        color_code = {'W': colors.to_rgb('blue'),
                      'L': colors.to_rgb('forestgreen'),
                      'H': colors.to_rgb('lightgreen'),
                      'D': colors.to_rgb('khaki')}

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

        herb_cell = self.animal_distribution.pivot('Row', 'Col', 'Herbivore')

        self.herb_density = self.ax_heat_h.imshow(herb_cell,
                                              vmax=self.cmax_animals
                                              ['Herbivore'],
                                              interpolation='nearest',
                                              cmap='Greens')
        self.ax_heat_h.set_title('Herbivore population density')


if __name__ == '__main__':
    pass
