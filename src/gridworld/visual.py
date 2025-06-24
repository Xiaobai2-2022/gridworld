import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

from src.gridworld.world import LandType

def draw_world(world, show_values=False):
    """
    Draw the World.grid as a colored image, optionally overlaying both
    waterValue (top) and grassValue (bottom) in each cell.
    """
    # map each LandType to an integer for coloring
    mapping = {
        LandType.PLAIN:      0,
        LandType.MOUNTAIN:   1,
        LandType.FRESHWATER: 2,
        LandType.GRASSLAND:  3,
    }
    grid_idx = np.zeros((world.length, world.width), dtype=int)
    for r in range(world.length):
        for c in range(world.width):
            grid_idx[r, c] = mapping[world.grid[r][c].land]

    cmap = ListedColormap(['tan', 'dimgray', 'skyblue', 'lightgreen'])
    plt.figure(figsize=(6,6))
    plt.imshow(grid_idx, cmap=cmap, interpolation='none')
    plt.xticks([]); plt.yticks([])

    if show_values:
        for r in range(world.length):
            for c in range(world.width):
                cell = world.grid[r][c]
                wv = cell.waterValue
                gv = cell.grassValue if cell.land == LandType.GRASSLAND else 0
                # pick text color so it’s legible
                base = grid_idx[r,c]
                color = 'white' if base in (1,2,3) else 'black'
                # two‐line label: water on first line, grass on second
                label = f"{wv}\n{gv}"
                plt.text(c, r, label,
                         ha='center', va='center',
                         color=color, fontsize=6)

    plt.title("World state" + (" (values shown)" if show_values else ""))
    plt.tight_layout()
    plt.show()
