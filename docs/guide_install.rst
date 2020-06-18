Guide
===================

Required packages
-------------------
The BioSim project supports Python 3.8. For the project to work properly the following
packages need to be installed: matplotlib, scipy, pandas, numpy, os, textwrap and subprocess.
Some of these packages usually come pre-installed on many Anaconda installation, but they
can also be install by using ``pip``::
    pip install matplotlib
    pip install scipy
    pip install pandas
    pip install numpy
    pip install os
    pip install textwrap
    pip install subprocess

The module also requires the program ``ffmpeg`` which is available from
`<https://ffmpeg.org>`_ or for conda install ffmpeg

Installing BioSim
--------------------
To install biosim via ``pip``, simply run the command::

    pip install BioSim_G13_Johan_Sabina

Alternatively, you can manually pull this repository and run the
``setup.py`` file::

    git clone https://github.com/Johanstab/BioSim_G13_Johan_Sabina.git
    cd BioSim_G13_Johan_Sabina
    python setup.py

References
----------
*   Moe, Y.M. (2019). *Group-Lasso*. `<https://group-lasso.readthedocs.io/en/latest/installation.html>`_.