# -*- coding: utf-8 -*-

""""
:mod: 'bisosim.visualization' provides the user with visualization functions for the island
         simulation

This script provides the users with the necessary function to make a full on visualization of the
given island when running a simulation. The script provides visualization of the island map, the
species count and the distribution of the different animals on the island.

This file can be imported as a module and contains the following class:

    *   Visualization - Class that contains all the visualization part and the updating of the
        graphs.

Notes
-----
    To run this script, its required to have 'numpy', 'matplotlib.pyplot' and 'textwrap"
    installed in the Python environment that your going to run this script in.
"""

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import matplotlib.pyplot as plt
import numpy as np
import textwrap

from matplotlib import colors


class Visualization:
    """Class for Visualization in Biosim"""

    def __init__(self, cmax=None, hist_dict=None):
        """Constructor that initiates Visualization class instances

        Parameters
        ----------
        cmax : dict
            Sets the max value of number of animals in the heat map distribution
        """
        self.cmax = cmax
        self.hist_dict = hist_dict
        self._has_run = False
        self._final_step = None
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
        self._fitness_axis = None
        self._age_axis = None
        self._weight_axis = None

        self._herb_line = None
        self._carn_line = None
        self._fitness_hist = None
        self._age_hist = None
        self._weight_hist = None

    def set_graphics(self, y_lim, x_lim, year):
        """Sets up the graphics for visualization of the different plots.

        Parameters
        ----------
        y_lim : int
            y-axis upper limit for graphics.

        x_lim : int
            x-axis upper limit for graphics.

        year : int
            the start year of the simulation graphics.
        """
        if self._fig is None:
            self._fig = plt.figure(constrained_layout=True, figsize=(8, 6))
            gs = self._fig.add_gridspec(5, 12)
            self._fig.tight_layout()
            plt.axis('off')

        if self._map_ax is None:
            self._map_ax = self._fig.add_subplot(gs[:2, 0:5])
            self._img_axis = None
            self._map_ax.set_yticklabels([])
            self._map_ax.set_xticklabels([])
            self._map_ax.title.set_text('Island')

        if self._year_ax is None:
            self._year_ax = self._fig.add_subplot(gs[:2, 5:7])
            self._text = self._year_ax.text(0.5, 0.5, f'Year: {year}',
                                            horizontalalignment='center',
                                            verticalalignment='center',
                                            transform=self._year_ax.transAxes,
                                            fontsize=14)
            self._year_ax.axis('off')

        if self._mean_ax is None:
            self._mean_ax = self._fig.add_subplot(gs[:2, 7:])
            self._mean_ax.set_ylim(0, y_lim)
            self._mean_ax.set_xlim(0, x_lim)
            self._mean_ax.set_xlabel('Years')
            self._mean_ax.set_ylabel('Nr animals pr species')
            self._mean_ax.title.set_text('Animal count')
        elif self._mean_ax is not None:
            self._mean_ax.set_xlim(0, x_lim)

        if self._herb_ax is None:
            self._herb_ax = self._fig.add_subplot(gs[2:4, :6])
            self._herb_axis = None
            self._herb_ax.set_yticklabels([])
            self._herb_ax.set_xticklabels([])
            self._herb_ax.title.set_text('Herbivore distribution')

        if self._carn_ax is None:
            self._carn_ax = self._fig.add_subplot(gs[2:4, 6:])
            self._carn_axis = None
            self._carn_ax.set_yticklabels([])
            self._carn_ax.set_xticklabels([])
            self._carn_ax.title.set_text('Carnivore distribution')

        if self._fitness_axis is None:
            self._fitness_axis = self._fig.add_subplot(gs[4:, :4])
            self._fitness_axis.set_title('Fitness')

        if self._age_axis is None:
            self._age_axis = self._fig.add_subplot(gs[4:, 4:8])
            self._age_axis.set_title('Age')

        if self._weight_axis is None:
            self._weight_axis = self._fig.add_subplot(gs[4:, 8:])
            self._weight_axis.set_title('Weight')

        if self._herb_line is None:
            herb_plot = self._mean_ax.plot(np.arange(0, x_lim),
                                           np.full(x_lim, np.nan),
                                           label='Herbivore')
            self._herb_line = herb_plot[0]
        elif self._herb_line is not None:
            self._final_step = x_lim

            xdata, ydata = self._herb_line.get_data()
            x_new = np.arange(xdata[-1] + 1, self._final_step)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._herb_line.set_data(np.hstack((xdata, x_new)),
                                         np.hstack((ydata, y_new)))

        if self._carn_line is None:
            carn_plot = self._mean_ax.plot(np.arange(0, x_lim),
                                           np.full(x_lim, np.nan),
                                           label='Carnivore')
            self._carn_line = carn_plot[0]
            self._mean_ax.legend(loc="upper right", prop={'size': 6})
        elif self._carn_line is not None:
            self._final_step = x_lim
            xdata, ydata = self._carn_line.get_data()
            x_new = np.arange(xdata[-1] + 1, self._final_step)
            if len(x_new) > 0:
                y_new = np.full(x_new.shape, np.nan)
                self._carn_line.set_data(np.hstack((xdata, x_new)),
                                         np.hstack((ydata, y_new)))

    def standard_map(self, default_geography):
        """Makes a visualisation of the given island geography. Assigns different colors to the
        different types of landscapes given.

        Parameters
        ----------
        default_geography : str
            Multiline string indicating geography of the island.
        """
        if self._has_run is not True:
            self._has_run = True
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
                axlg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1, edgecolor='none',
                                             facecolor=color_code[name[0]]))
                axlg.text(0.35, ix * 0.2, name, transform=axlg.transAxes)

    def update_herb_heatmap(self, df):
        """Updates the value of how many herbivores that is present i each cell of the island every
        year. This is used to show the herbivore distribution on the island.

        Parameters
        ----------
        df : df
            Dataframe that contains the information of how many herbivores that is in each cell of
            the island.
        """
        if self._herb_axis is not None:
            self._herb_axis.set_data(df.pivot('Row', 'Col', 'Herbivore'))
        else:
            self._herb_axis = self._herb_ax.imshow(df.pivot('Row', 'Col', 'Herbivore'),
                                                   interpolation='nearest',
                                                   vmin=0,
                                                   vmax=self.cmax['Herbivore'])
            self._herb_ax.figure.colorbar(self._herb_axis, ax=self._herb_ax,
                                          orientation='vertical',
                                          fraction=0.07, pad=0.04)

    def update_carn_heatmap(self, df):
        """Updates the value of how many carnivores that is present i each cell of the island every
        year. This is used to show the carnivores distribution on the island.

        Parameters
        ----------
        df : df
            Dataframe that contains the information of how many carnivores that is in each cell of
            the island.
        """
        if self._carn_axis is not None:
            self._carn_axis.set_data(df.pivot('Row', 'Col', 'Carnivore'))
        else:
            self._carn_axis = self._carn_ax.imshow(df.pivot('Row', 'Col', 'Carnivore'),
                                                   interpolation='nearest',
                                                   vmin=0,
                                                   vmax=self.cmax['Carnivore'])
            self._carn_ax.figure.colorbar(self._carn_axis, ax=self._carn_ax,
                                          orientation='vertical',
                                          fraction=0.07, pad=0.04)

    def update_animal_count(self, num_herbs, num_carns, year):
        """Updates the total animal count graph on the island. The species are sorted in total
        herbivores and total carnivores.

        Parameters
        ----------
        num_herbs : int
                Total number of herbivores present on the island the current year.

        num_carns : int
                Total number of carnivores present on the island the current year.

        year      : int
                The current year of the simulation of the island
        """
        herb = self._herb_line.get_ydata()
        herb[year] = num_herbs
        self._herb_line.set_ydata(herb)
        if self._mean_ax.get_ylim()[1] < num_herbs:
            self._mean_ax.autoscale(enable=True, axis='y')

        carn = self._carn_line.get_ydata()
        carn[year] = num_carns
        self._carn_line.set_ydata(carn)

    def update_year_count(self, island_year):
        """Updates the year counter in the visualization.

        Parameters
        ----------
        island_year : int
                The current year of the simulation.
        """
        self._text.set_text(f'Year:{island_year}')

    def update_fitness(self, data_1, data_2):
        if self._fitness_hist is None:
            n = np.ceil((self.hist_dict['fitness']['max'] - 0) / self.hist_dict['fitness']['delta'])
            self._fitness_axis.clear()
            self._fitness_axis.set_title('Fitness')
            self._fitness_axis.hist(data_1['fitness'], bins=int(n),
                                    range=(0, self.hist_dict['fitness']['max']),
                                    histtype='step', color='b')
            self._fitness_axis.hist(data_2['fitness'], bins=int(n),
                                    range=(0, self.hist_dict['fitness']['max']),
                                    histtype='step', color='r')

    def update_age(self, data_1, data_2):
        if self._age_hist is None:
            n = np.ceil((self.hist_dict['age']['max'] - 0) / self.hist_dict['age']['delta'])
            self._age_axis.clear()
            self._age_axis.set_title('Age')
            self._age_axis.hist(data_1['age'], bins=int(n),
                                range=(0, self.hist_dict['age']['max']),
                                histtype='step', color='b')
            self._age_axis.hist(data_2['age'], bins=int(n),
                                range=(0, self.hist_dict['age']['max']),
                                histtype='step', color='r')

    def update_weight(self, data_1, data_2):
        if self._weight_hist is None:
            n = np.ceil((self.hist_dict['weight']['max'] - 0) / self.hist_dict['weight']['delta'])
            self._weight_axis.clear()
            self._weight_axis.set_title('Weight')
            self._weight_axis.hist(data_1['weight'], bins=int(n),
                                   range=(0, self.hist_dict['weight']['max']),
                                   histtype='step', color='b')
            self._weight_axis.hist(data_2['weight'], bins=int(n),
                                   range=(0, self.hist_dict['weight']['max']),
                                   histtype='step', color='r')

    def update_graphics(self, df, num_animals, year, data_1, data_2):
        """Updates the graphs in the visualization for each year of the simulation.

        Parameters
        ----------
        df : df
                Dataframe that contains the distribution of the different spices on the island.

        num_animals : dict
                Dictionary that contains the number of Herbivores and the number of Carnivores,
                the current year.

        year : int
                The current year of the simulation
        """
        self.update_herb_heatmap(df)
        self.update_carn_heatmap(df)
        self.update_animal_count(num_animals['Herbivore'],
                                 num_animals['Carnivore'],
                                 year)
        self.update_year_count(year)
        self.update_fitness(data_1, data_2)
        self.update_age(data_1, data_2)
        self.update_weight(data_1, data_2)

        plt.pause(1e-3)
