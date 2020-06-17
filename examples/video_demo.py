from biosim.simulation import BioSim

DEFAULT_IMAGE_BASE = r'/Users/sabinal/Documents/INF200 JUNI/Bilder og videoer/bio'


sim = BioSim(ymax_animals=300,
             cmax_animals={'Herbivore': 20, 'Carnivore': 20},
             img_base=DEFAULT_IMAGE_BASE)
sim.simulate(10, 1, 1)

sim.make_movie()