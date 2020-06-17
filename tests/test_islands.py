# -*- coding: utf-8 -*-

__author__ = "Johan Stabekk, Sabina Langås"
__email__ = "johansta@nmbu.no, sabinal@nmbu.no"

import pytest
from biosim.island import Island
from biosim.landscapes import Lowland, Highland, Water, Desert


def test_default_init():
    """Tests that map and population is added in init function."""
    default_pop = [
        {
            "loc": (2, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20.0} for _ in range(20)],
        },
        {
            "loc": (2, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20.0} for _ in range(50)],
        },
    ]
    default_geography = """\
                            WWW
                            WLW
                            WWW"""
    island = Island(default_geography, default_pop)
    assert island.initial_pop is not None
    assert isinstance(island.island_map[(2, 2)], Lowland)
    assert len(island.island_map[(2, 2)].herbivore_list) == 50
    assert len(island.island_map[(2, 2)].carnivore_list) == 20


def test_wrong_landscapes_key():
    """Test that wrong landscape keys raise ValueError."""
    default_geography = """\
                            WWW
                            WRW
                            WWW"""

    with pytest.raises(ValueError):
        Island(island_map=default_geography)


def test_wrong_boundaries1():
    """Test that adding a cell that is not water at the edges raises ValueError."""
    default_geography = """\
                            HWW
                            WLW
                            WWW"""
    with pytest.raises(ValueError):
        Island(island_map=default_geography)
    default_geography = """\
                            WWW
                            LLW
                            WWW"""
    with pytest.raises(ValueError):
        Island(island_map=default_geography)


def test_wrong_length():
    """Test that a map with inconsistent line length raises ValueError."""
    default_geography = """\
                            WWW
                            WLLW
                            WWW"""
    with pytest.raises(ValueError):
        Island(island_map=default_geography)


@pytest.fixture
def plain_landscape():
    """Sets a plain landscape to use in tests below."""
    return Island(island_map="WWWW\nWLHW\nWWWW", ini_pop=[])


def test_set_population_none(plain_landscape):
    """Test that set population with no input returns no animals."""
    plain_landscape.set_population_in_cell()
    assert plain_landscape.nr_animals() == 0


def test_wrong_key_set_pop_raise_value_error(plain_landscape):
    """Test that input with a location that doesn't exist raises ValueError."""
    default_pop = [
        {
            "loc": (0, 0),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20.0} for _ in range(5)],
        },
        {
            "loc": (0, 0),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20.0} for _ in range(5)],
        },
    ]
    with pytest.raises(ValueError):
        plain_landscape.set_population_in_cell(default_pop)


def test_pos_not_passable_raise_value_error(plain_landscape):
    """Test that setting population in cells that isn't passable raises ValueError. """
    default_pop = [
        {
            "loc": (1, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20.0} for _ in range(5)],
        },
        {
            "loc": (1, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20.0} for _ in range(5)],
        },
    ]
    with pytest.raises(ValueError):
        plain_landscape.set_population_in_cell(default_pop)


def test_get_nr_animals_pr_species(plain_landscape):
    """Test getting number of animals per species returns right amount."""
    default_pop = [
        {
            "loc": (2, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20.0} for _ in range(20)],
        },
        {
            "loc": (2, 3),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20.0} for _ in range(20)],
        },
    ]
    plain_landscape.set_population_in_cell(default_pop)
    nr_animals = plain_landscape.nr_animals_pr_species()
    assert nr_animals["Herbivore"] == 20
    assert nr_animals["Carnivore"] == 20


def test_get_nr_animals(plain_landscape):
    """Test that get number of animals returns the right number of animals."""
    default_pop = [
        {
            "loc": (2, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20.0} for _ in range(10)],
        },
        {
            "loc": (2, 3),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20.0} for _ in range(20)],
        },
    ]
    plain_landscape.set_population_in_cell(default_pop)
    assert plain_landscape.nr_animals() == 30


def test_next_cell(mocker):
    """Test to see if next cell will be as intended when mocking a choice and that it returns a
    tuple."""
    mocker.patch("numpy.random.choice", return_value=0)
    next_cell = Island.next_cell((2, 2))
    assert next_cell == (1, 2)


def test_migrate_animals(plain_landscape, mocker):
    """Tests that animals migrates to a new cell and that they are removed from
    the original cell"""
    mocker.patch("numpy.random.choice", return_value=3)
    mocker.patch("numpy.random.random", return_value=0)
    default_pop = [
        {
            "loc": (2, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20.0} for _ in range(5)],
        },
        {
            "loc": (2, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20.0} for _ in range(5)],
        },
    ]
    plain_landscape.set_population_in_cell(default_pop)
    pop_before = len(plain_landscape.island_map[(2, 2)].herbivore_list) + len(
        plain_landscape.island_map[(2, 2)].carnivore_list
    )
    plain_landscape.migrate_animals((2, 2))
    pop_after = len(plain_landscape.island_map[(2, 2)].herbivore_list) + len(
        plain_landscape.island_map[(2, 2)].carnivore_list
    )
    assert pop_before != pop_after
    assert pop_after == 0
    assert len(plain_landscape.island_map[(2, 3)].herbivore_list) == 5
    assert len(plain_landscape.island_map[(2, 3)].carnivore_list) == 5


def test_migrate_break_if_not_passable(plain_landscape, mocker):
    """Test that migrate will break if the cell that is chosen isn't passable and that
    the original population will stay in the same cell."""
    mocker.patch("numpy.random.choice", return_value=2)
    default_pop = [
        {
            "loc": (2, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20.0} for _ in range(5)],
        },
        {
            "loc": (2, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20.0} for _ in range(5)],
        },
    ]
    plain_landscape.set_population_in_cell(default_pop)
    pop_before = len(plain_landscape.island_map[(2, 2)].herbivore_list) + len(
        plain_landscape.island_map[(2, 2)].carnivore_list
    )
    plain_landscape.migrate_animals((2, 2))
    pop_after = len(plain_landscape.island_map[(2, 2)].herbivore_list) + len(
        plain_landscape.island_map[(2, 2)].carnivore_list
    )
    assert pop_before == pop_after
    assert type(plain_landscape.island_map[2, 1]) is Water


def test_reset_migration(plain_landscape, mocker):
    """Test that after migration, the animals that has migrated changes their value of has_moved
    from True to False."""
    mocker.patch("numpy.random.choice", return_value=3)
    mocker.patch("numpy.random.random", return_value=0)
    default_pop = [
        {
            "loc": (2, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20.0} for _ in range(2)],
        },
        {
            "loc": (2, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20.0} for _ in range(2)],
        },
    ]
    plain_landscape.set_population_in_cell(default_pop)
    has_not_moved = plain_landscape.island_map[(2, 2)].herbivore_list[0].has_moved
    plain_landscape.migrate_animals((2, 2))
    has_moved = plain_landscape.island_map[(2, 3)].herbivore_list[0].has_moved
    plain_landscape.reset_migration()
    reset_moved = plain_landscape.island_map[(2, 3)].herbivore_list[0].has_moved

    assert has_not_moved is not has_moved
    assert has_moved is not reset_moved
    assert has_not_moved is reset_moved


def test_island_cycle(plain_landscape):
    """Test that we can simulate a cycle on the island."""
    default_pop = [
        {
            "loc": (2, 2),
            "pop": [{"species": "Carnivore", "age": 5, "weight": 20.0} for _ in range(2)],
        },
        {
            "loc": (2, 2),
            "pop": [{"species": "Herbivore", "age": 5, "weight": 20.0} for _ in range(2)],
        },
    ]
    plain_landscape.set_population_in_cell(default_pop)
    plain_landscape.cycle_island()
