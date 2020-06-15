# -*- coding: utf-8 -*-

"""
mod: 'bisosim.landscapesl' gives the user information about different kinds of cells on Rossumøya,
      and which kind of information these cells holds.

The island that is Rossumøya, is dived into squared formed cells. These cells have there own
numerical location and one type of valid landscape. The superclass and subclasses holds the
information that is stored in the different cells that makes up Rossumøya.

This file can be imported as a module and contains the following classes:

    *   Landscape - Superclass that contains basic characteristics that all of the cell types in
        Rossumøya has in common. The function that will make the 'cycle" of Rossumøya work, could
        also be find her.

    *   Desert(Landscape) - Subclass of Landscape with characteristics for the cell type Desert.

    *   Lowland(Landscape) - Subclass of Landscape with characteristics for the cell type Jungle.

    *   Highland(Landscape) - Subclass of Landscape with characteristics for the cell type Highland.

    *   Water(Landscape) - Subclass of Landscape with characteristics for the cell type Ocean.

Notes
-----
    To run this script, its required to have 'numpy' installed in the Python environment that
    your going to run this script in.
"""

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import numpy as np

from .animals import Herbivore, Carnivore


class Landscape:
    """Superclass for landscape cells in BioSim"""
    params = {}

    @classmethod
    def set_params(cls, new_params):
        """This method gives the ability to change the default params of the different landscape
        cells.

        Parameters
        ----------
        new_params : dict
                Dictionary that contains new parameters for the landscape cell.
        """
        for param in new_params:
            if param not in cls.params:
                raise KeyError("Invalid parameter name: " + new_params[0])

            if param == "f_max" and new_params["f_max"] < 0:
                raise ValueError("f_max must be positive")

        cls.params.update(new_params)

    def __init__(self):
        """Constructor that initiates class Landscapes."""
        self.herbivore_list = []
        self.carnivore_list = []
        self.available_food = 0

    def set_population(self, input_list):
        """Sets the populations of animals.

        Parameters
        ----------
        input_list : list
                List of dictionaries containing Herbivores and Carnivores.
        """
        for animal in input_list:
            if animal['species'] == 'Herbivore':
                self.herbivore_list.append(Herbivore(age=animal["age"], weight=animal["weight"]))
            elif animal['species'] == 'Carnivore':
                self.carnivore_list.append(Carnivore(age=animal["age"], weight=animal["weight"]))

    def add_population(self, animal):
        """Makes it possible to add new animal populations to
        different landscape cells.

        Parameters
        ----------
        animal: dict
            Dict containing information about the animal that being added to the landscape cell.
        """
        if type(animal).__name__ == 'Herbivore':
            self.herbivore_list.append(animal)
        elif type(animal).__name__ == 'Carnivore':
            self.carnivore_list.append(animal)

    def food_grows(self):
        """Updates food for each year."""
        if type(self) == Lowland:
            self.available_food = self.params['f_max']
        elif type(self) == Highland:
            self.available_food = self.params['f_max']

    def herbivore_eats(self):
        """Cycle where all herbivores eats fodder in a random order according to how much
        the parameters defines. If there is no fodder left then no more herbivores get to eat."""
        np.random.shuffle(self.herbivore_list)

        for herbivore in self.herbivore_list:
            if self.available_food == 0:
                break
            if self.available_food >= herbivore.params['F']:
                herbivore.eats(herbivore.params['F'])
                self.available_food -= herbivore.params['F']
            if self.available_food < herbivore.params['F']:
                herbivore.eats(self.available_food)
                self.available_food = 0

    def carnivore_eats(self):
        """Cycle where all carnivores eats herbivores. The fittest carnivore tries to kill the
        least fit herbivore and continues until it has eaten according to the parameters. When
        the fittest carnivore has is satisfied the next in order of fitness will proceed until
        until everyone is satisfied or all herbivores are killed."""
        self.carnivore_list.sort(key=lambda animal: animal.fitness, reverse=True)
        self.herbivore_list.sort(key=lambda animal: animal.fitness)

        for carnivore in self.carnivore_list:
            self.herbivore_list = carnivore.eat(self.herbivore_list)

    def herbivore_reproduce(self):
        """Gives the herbivore the ability to reproduce. The function checks that at least two
        herbivore are present in the cell, so reproduction can happen. If birth function returns
        True, a new herbivore will be made. It will be put in a list of new herbivores,
        before its added to the rest of the population."""
        nr_animals = len(self.herbivore_list)

        if nr_animals < 2:
            return False

        new_babies = []
        for herbivore in self.herbivore_list:
            new_baby = herbivore.birth(nr_animals)
            if new_baby is not None:
                new_babies.append(new_baby)

        self.herbivore_list.extend(new_babies)

    def carnivore_reproduce(self):
        """Gives the carnivore the ability to reproduce. The function checks that at least two
        carnivore are present in the cell, so reproduction can happen. If birth function returns
        True, a new carnivore will be made. It will be put in a list of new carnivores,
        before its added to the rest of the population."""
        nr_animals = len(self.carnivore_list)

        if nr_animals < 2:
            return False

        new_babies = []
        for carnivore in self.carnivore_list:
            new_baby = carnivore.birth(nr_animals)
            if new_baby is not None:
                new_babies.append(new_baby)

        self.carnivore_list.extend(new_babies)

    def animals_die(self):
        """Checks if a animal should die or not and removes the dead animal from the lists."""
        self.herbivore_list = [animal for animal in self.herbivore_list if not animal.death()]
        self.carnivore_list = [animal for animal in self.carnivore_list if not animal.death()]

    def animals_age(self):
        """The animals increase one year in age."""
        for herbivore in self.herbivore_list:
            herbivore.aging()
        for carnivore in self.carnivore_list:
            carnivore.aging()

    def animals_lose_weight(self):
        """The animals loose weigh.t"""
        for herbivore in self.herbivore_list:
            herbivore.weight_loss()
        for carnivore in self.carnivore_list:
            carnivore.weight_loss()

    def animals_migrate(self):
        """Deiced if a animals will migrate the current year or not. Checks if the animal already
        have moved the current year. If the animal has not moved yet and the move function returns
        True, the animal will be put in lists of animals that want to move the current year.

        Returns
        -------
        moved_herbs : list
            List of dicts over the herbivores that want to move current year.

        moved_carns : list
            List of dicts over the carnivores that want to move current year.
        """
        moved_herbs = []
        moved_carns = []

        for herb in self.herbivore_list:
            if herb.has_moved is not True and herb.move():
                moved_herbs.append(herb)

        for carn in self.carnivore_list:
            if carn.has_moved is not True and carn.move():
                moved_carns.append(carn)

        return moved_herbs, moved_carns

    def reset_migrate(self):
        """Reset the migration for all animals, so they will able to move the next year."""
        for herb in self.herbivore_list:
            herb.has_moved = False
        for carn in self.carnivore_list:
            carn.has_moved = False


class Lowland(Landscape):
    """Class instance of class Landscape for the cell type Lowland."""
    params = {'f_max': 800}
    passable = True

    def __init__(self):
        """Constructor that initiate class instance Lowland."""
        super().__init__()


class Highland(Landscape):
    """Class instance of class Landscape for the cell type Highland."""
    params = {'f_max': 300}
    passable = True

    def __init__(self):
        """Constructor that initiate class instance Highland."""
        super().__init__()


class Water(Landscape):
    """Class instance of class Landscape for the cell type Water."""
    passable = False

    def __init__(self):
        """Constructor that initiate class instance Water."""
        super().__init__()


class Desert(Landscape):
    """Class instance of class Landscape for the cell type Desert"""
    passable = True

    def __init__(self):
        """Constructor that initiate class instance Desert."""
        super().__init__()

