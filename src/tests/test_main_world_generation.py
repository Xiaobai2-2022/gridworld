# src/tests/test_ipython_world_simulation.py

import time
import pytest
from IPython.display import clear_output
from src.gridworld.world import World, Cell, LandType
from src.gridworld.visual import draw_world

def build_custom_layout(size: int):
    layout = [[Cell(LandType.PLAIN) for _ in range(size)] for _ in range(size)]
    # mountains
    layout[1][1] = Cell(LandType.MOUNTAIN)
    layout[1][2] = Cell(LandType.MOUNTAIN)
    layout[2][2] = Cell(LandType.MOUNTAIN)
    layout[2][3] = Cell(LandType.MOUNTAIN)
    layout[2][4] = Cell(LandType.MOUNTAIN)
    layout[3][4] = Cell(LandType.MOUNTAIN)
    layout[4][4] = Cell(LandType.MOUNTAIN)
    layout[4][5] = Cell(LandType.MOUNTAIN)
    layout[4][6] = Cell(LandType.MOUNTAIN)
    layout[4][7] = Cell(LandType.MOUNTAIN)
    layout[4][8] = Cell(LandType.MOUNTAIN)
    layout[4][9] = Cell(LandType.MOUNTAIN)
    layout[4][10] = Cell(LandType.MOUNTAIN)
    layout[4][11] = Cell(LandType.MOUNTAIN)
    layout[4][12] = Cell(LandType.MOUNTAIN)
    layout[4][12] = Cell(LandType.MOUNTAIN)
    layout[5][8] = Cell(LandType.MOUNTAIN)
    layout[6][8] = Cell(LandType.MOUNTAIN)
    layout[7][8] = Cell(LandType.MOUNTAIN)
    layout[8][8] = Cell(LandType.MOUNTAIN)
    layout[9][8] = Cell(LandType.MOUNTAIN)
    layout[10][8] = Cell(LandType.MOUNTAIN)
    layout[11][8] = Cell(LandType.MOUNTAIN)
    layout[12][8] = Cell(LandType.MOUNTAIN)
    layout[13][8] = Cell(LandType.MOUNTAIN)
    layout[14][8] = Cell(LandType.MOUNTAIN)
    # lake
    layout[5][7] = Cell(LandType.FRESHWATER)
    layout[5][9] = Cell(LandType.FRESHWATER)
    layout[6][9] = Cell(LandType.FRESHWATER)
    layout[5][10] = Cell(LandType.FRESHWATER)
    # initial grass seed
    layout[15][8] = Cell(LandType.GRASSLAND)
    return layout

def test_ipython_simulation_visual():
    size = 20
    layout = build_custom_layout(size)
    world = World(width=size, length=size, layout=layout)

    steps = 200
    for step in range(steps):
        clear_output(wait=True)
        print(f"Step {step+1}/{steps}")
        draw_world(world, show_values=True)
        world.update()
        time.sleep(0.5)

    # assert that grass has indeed spread into (1,2)
    cell = world.get_cell(1, 2)
    assert cell.land == LandType.GRASSLAND
    assert cell.grassValue >= 1
