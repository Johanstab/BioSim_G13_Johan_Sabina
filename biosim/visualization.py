# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import textwrap
import matplotlib.pyplot as plt
from matplotlib import colors
import pandas as pd
import numpy as np


class Visualization:

    def __init__(self, cmax=None):
        self.cmax = cmax
        self._step = 0
        self._fig = None
        self._map_ax = None
        self._img_axis = None
        self._mean_ax = None
        self._year_ax = None
        self._text = None
        self._herb_ax = None
        self._carn_ax = None
        self._herb_axis = None
        self._carn_axis = None

        self._herb_line = None
        self._carn_line = None
        self._mean_line = None
        self._final_step = None

    def set_graphics(self, y_lim, x_lim, year):

        if self._fig is None:
            self._fig = plt.figure(figsize=(16, 9))
            self._fig.tight_layout()
            plt.axis('off')

        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(2, 3, 1)
            self._img_axis = None
            self._map_ax.set_yticklabels([])
            self._map_ax.set_xticklabels([])
            self._map_ax.title.set_text('Island')

        if self._year_ax is None:
            self._year_ax = self._fig.add_subplot(2, 3, 2)
            self._text = self._year_ax.text(0.5, 0.5, f'Year: {year}',
                                            horizontalalignment='center',
                                            verticalalignment='center',
                                            transform=self._year_ax.transAxes,
                                            fontsize=14)
            self._year_ax.axis('off')

        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(2, 3, 3)
            self._mean_ax.set_ylim(0, y_lim)
            self._mean_ax.set_xlim(0, x_lim)
            self._mean_ax.set_xlabel('Years')
            self._mean_ax.set_ylabel('Nr animals pr species')
            self._mean_ax.title.set_text('Animal count')
            self._mean_ax.legend()
        elif self._mean_ax is not None:
            self._mean_ax.set_xlim(0, x_lim)

        if self._herb_ax is None:
            self._herb_ax = self._fig.add_subplot(2, 3, 4)
            self._herb_axis = None
            self._herb_ax.set_yticklabels([])
            self._herb_ax.set_xticklabels([])
            self._herb_ax.title.set_text('Herbivore distribution')

        if self._carn_ax is None:
            self._carn_ax = self._fig.add_subplot(2, 3, 5)
            self._carn_axis = None
            self._carn_ax.set_yticklabels([])
            self._carn_ax.set_xticklabels([])
            self._carn_ax.title.set_text('Carnivore distribution')

        if self._herb_line is None:
            herb_plot = self._mean_ax.plot(np.arange(0, x_lim),
                                           np.full(x_lim, np.nan),
                                           label='Herbivore')
            self._herb_line = herb_plot[0]
        elif self._herb_line is not None:
            herb_plot = self._mean_ax.plot(np.arange(0, x_lim),
                                           np.full(x_lim, np.nan),
                                           label='Herbivore after break')
            self._herb_line = herb_plot[0]

        if self._carn_line is None:
            carn_plot = self._mean_ax.plot(np.arange(0, x_lim),
                                           np.full(x_lim, np.nan),
                                           label='Carnivore')
            self._carn_line = carn_plot[0]
            self._mean_ax.legend(loc="upper right", prop={'size': 6})
        elif self._carn_line is not None:
            carn_plot = self._mean_ax.plot(np.arange(0, x_lim),
                                           np.full(x_lim, np.nan),
                                           label='Carnivore after break')
            self._carn_line = carn_plot[0]
            self._mean_ax.legend(loc="upper right", prop={'size': 6})

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
        for ix, name in enumerate(('W', 'L', 'H', 'D')):
            axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                         edgecolor='none',
                                         facecolor=color_code[name[0]]))
            axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

    def update_herb_heatmap(self, df):

        if self._herb_axis is not None:
            self._herb_axis.set_data(df.pivot('Row', 'Col', 'Herbivore'))
        else:
            self._herb_axis = self._herb_ax.imshow(df.pivot('Row', 'Col', 'Herbivore'),
                                                   interpolation='nearest',
                                                   cmap="Greens", vmin=0,
                                                   vmax=self.cmax['Herbivore'])
            self._herb_ax.figure.colorbar(self._herb_axis, ax=self._herb_ax,
                                          orientation='vertical',
                                          fraction=0.07, pad=0.04)

    def update_carn_heatmap(self, df):

        if self._carn_axis is not None:
            self._carn_axis.set_data(df.pivot('Row', 'Col', 'Carnivore'))
        else:
            self._carn_axis = self._carn_ax.imshow(df.pivot('Row', 'Col', 'Carnivore'),
                                                   interpolation='nearest',
                                                   cmap="OrRd", vmin=0,
                                                   vmax=self.cmax['Carnivore'])
            self._carn_ax.figure.colorbar(self._carn_axis, ax=self._carn_ax,
                                          orientation='vertical',
                                          fraction=0.07, pad=0.04)

    def update_animal_count(self, num_herbs, num_carns, year):
        herb = self._herb_line.get_ydata()
        herb[year] = num_herbs
        self._herb_line.set_ydata(herb)
        if self._mean_ax.get_ylim()[1] < num_herbs:
            self._mean_ax.autoscale(enable=True, axis='y')

        carn = self._carn_line.get_ydata()
        carn[year] = num_carns
        self._carn_line.set_ydata(carn)

    def update_year_count(self, island_year):
        self._text.set_text(f'Year:{island_year}')

    def update_graphics(self, df, num_animals, year):
        self.update_herb_heatmap(df)
        self.update_carn_heatmap(df)
        self.update_animal_count(num_animals['Herbivore'],
                                 num_animals['Carnivore'],
                                 year)
        self.update_year_count(year)

        plt.pause(1e-3)


if __name__ == '__main__':
    pass
