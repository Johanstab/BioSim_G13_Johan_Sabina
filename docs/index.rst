.. BioSim_G13 documentation master file, created by
   sphinx-quickstart on Fri Jun  5 08:47:52 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Modelling the Ecosystem of Rossumøya
==============================================
This library provides the computer programs for the simulation of population
dynamics on Rossumøya.

Summary
--------------
The long term goal is to preserve Rossumøya asa nature park for future generations. The  ecosystem  on  Rossumøya  is
characterized by several different landscape types, lowland, highland and desert. The fauna includes only two species,
one species of herbivores (plant  eaters), and one of carnivores (predators).In order to investigate if both species can
survive in the long term we have made a simulation which runs for a given amount of years. After the simulation,
one can obtain a status information which include: number of years that has been simulated,total number of animals on
the island and total number of animals per species. One is also able to visualize the simulation results while the
simulation runs. The graphics window include: the island's geography,total number of animals per species as graph,
distribution heat maps for the number of animals per cell and simulation year. [1]_

Installation
------------------
To make the BioSim run as smooth as possible, its required to have some libraries and setups
installed. Read about the requirements and how to get them :doc:`here.<guide_install>`

.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Installation

   guide_install

Modules
---------------------

The modules and the source code for this project can be reached by clicking
on the links below.

*  :doc:`The Simulation module <simulation>`

*  :doc:`The Visualization module <visualization>`

*  :doc:`The Island module <island>`

*  :doc:`The Landscapes module <landscapes>`

*  :doc:`The Animals module <animals>`


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Modules

   simulation
   visualization
   island
   landscapes
   animals

References
----------
.. [1] Plesser, H. E. (2020). *Modelling the Ecosystem of Rossumøya*.

