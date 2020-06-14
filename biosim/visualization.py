# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import textwrap
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd
import numpy as np


class Visualization:

    def __init__(self):
        self.dataframe = None
        self._step = 0
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._mean_ax = None
        self._herb_ax = None
        self._carn_ax = None
        self._herb_axis = None
        self._carn_axis = None

        self._herb_line = None
        self._carn_line = None

    def set_graphics(self, y_lim, x_lim):

        if self._fig is None:
            self._fig = plt.figure(figsize=(16, 9))
            plt.axis('off')

        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(2, 2, 1)
            self._img_axis = None
            self._map_ax.set_yticklabels([])
            self._map_ax.set_xticklabels([])
            self._map_ax.title.set_text('Island Map')

        if self._herb_ax is None:
            self._herb_ax = self._fig.add_subplot(2, 2, 2)
            self._herb_axis = None
            self._herb_ax.set_yticklabels([])
            self._herb_ax.set_xticklabels([])
            self._herb_ax.title.set_text('Herbivore HeatMap')

        if self._carn_ax is None:
            self._carn_ax = self._fig.add_subplot(2, 2, 3)
            self._carn_axis = None
            self._carn_ax.set_yticklabels([])
            self._carn_ax.set_xticklabels([])
            self._carn_ax.title.set_text('Carnivore HeatMap')

        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(2, 2, 4)
            self._mean_ax.set_ylim(0, y_lim)
            self._mean_ax.set_xlim(0, x_lim)
            self._mean_ax.set_xlabel('Years')
            self._mean_ax.set_ylabel('Number of Species')
            self._mean_ax.title.set_text('Number of Species')
            self._mean_ax.legend()

        if self._herb_line is None:
            herb_plot = self._mean_ax.plot(np.arange(0, x_lim),
                                           np.full(x_lim, np.nan),
                                           label='Herbivore')
            self._herb_line = herb_plot[0]

        if self._carn_line is None:
            carn_plot = self._mean_ax.plot(np.arange(0, x_lim),
                                           np.full(x_lim, np.nan),
                                           label='Carnivore')
            self._carn_line = carn_plot[0]
            self._mean_ax.legend(loc="upper right")

    def animal_distribution(self, island_map):

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

    def standard_map(self, default_geography):
        island_string = default_geography
        string_map = textwrap.dedent(island_string)
        string_map.replace('\n', ' ')

        color_code = {'W': colors.to_rgb('blue'),
                      'L': colors.to_rgb('darkgreen'),
                      'H': colors.to_rgb('lightgreen'),
                      'D': colors.to_rgb('lightyellow')}

        island_map = [[color_code[column] for column in row]
                      for row in string_map.splitlines()]

        self._map_ax.imshow(island_map, interpolation='nearest')
        axlg = self._fig.add_axes([0.03, 0.525, 0.1, 0.4])
        axlg.axis('off')
        for ix, name in enumerate(('W', 'L', 'H',
                                   'D')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=color_code[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

    # def heat_map_herbivore(self):
    #
    #     herb_cell = self.dataframe.pivot('Row', 'Col', 'Herbivore')
    #     fig = plt.figure()
    #
    #     ax_heat_h = fig.add_subplot(224)
    #
    #     ax_heat_h.imshow(herb_cell,
    #                      vmax=100,
    #                      interpolation='nearest',
    #                      cmap='Greens')
    #
    #     ax_heat_h.set_title('Herbivore population density')

    # def heat_map_carnivore(self):
    #
    #     carn_cell = self.dataframe.pivot('Row', 'Col', 'Carnivore')
    #
    #     self.ax_heat_c.imshow(carn_cell,
    #                           vmax=75,
    #                           interpolation='nearest',
    #                           cmap='Reds')
    #     ax_heat_c.set_title('Carnivore population density')

    def update_herb_ax(self, herb_limit):

        if self._herb_axis is not None:
            self._herb_axis.set_data(self.dataframe.pivot('Row', 'Col', 'Herbivore'))
        else:
            self._herb_axis = self._herb_ax.imshow(self.dataframe.pivot('Row', 'Col', 'Herbivore'),
                                                   interpolation='nearest',
                                                   cmap="Greens", vmin=0,
                                                   vmax=herb_limit)
            self._herb_ax.figure.colorbar(self._herb_axis, ax=self._herb_ax,
                                          orientation='horizontal',
                                          fraction=0.07, pad=0.04)

    def update_carn_ax(self, carn_limit):

        if self._carn_axis is not None:
            self._carn_axis.set_data(self.dataframe.pivot('Row', 'Col', 'Carnivore'))
        else:
            self._carn_axis = self._carn_ax.imshow(self.dataframe.pivot('Row', 'Col', 'Carnivore'),
                                                   interpolation='nearest',
                                                   cmap="OrRd", vmin=0,
                                                   vmax=carn_limit)
            self._carn_ax.figure.colorbar(self._carn_axis, ax=self._carn_ax,
                                          orientation='horizontal',
                                          fraction=0.07, pad=0.04)

    def update_mean_ax(self, herb_num, carn_num):
        ydata = self._herb_line.get_ydata()
        ydata[self._step] = herb_num
        self._herb_line.set_ydata(ydata)

        ydata = self._carn_line.get_ydata()
        ydata[self._step] = carn_num
        self._carn_line.set_ydata(ydata)
        self._step += 1

    def update_graphics(self, herb_pos, carn_pos, num_animals_per_sp,
                        col_limits):

        herb_limit = col_limits['Herbivore']
        carn_limit = col_limits['Carnivore']
        self.update_herb_ax(herb_pos, herb_limit)
        self.update_carn_ax(carn_pos, carn_limit)
        self.update_mean_ax(num_animals_per_sp["Herbivore"],
                            num_animals_per_sp["Carnivore"])
        #plt.pause(1e-9)


if __name__ == '__main__':
    pass
