# -*- coding: utf-8 -*-

__author__ = 'Johan Stabekk, Sabina Langås'
__email__ = 'johansta@nmbu.no, sabinal@nmbu.no'

import random

"""
Here we will  
"""


class Landscapes:
    def __init__(self):
        "common traits are size."
        pass


class Lowland(Landscapes):
    passable = True
    f_max = 800.0

    def __init__(self):
        super().__init__()


class Highland(Landscapes):
    passable = True
    f_max = 300.0

    def __init__(self):
        super().__init__()


class Water(Landscapes):
    passable = False

    def __init__(self):
        super().__init__()


class Desert(Landscapes):
    passable = True
    f_max = 0

    def __init__(self):
        super().__init__()
