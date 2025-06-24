from enum import Enum
import numpy as np
from collections import deque

class LandType(Enum):
    PLAIN = 0               # Regular Terrain
    MOUNTAIN = 1            # Impossible Terrain
    FRESHWATER = 128        # Lake, contains water
    GRASSLAND = 256         # Grassland, contains grass

class Cell:
    def __init__(self, land: LandType = LandType.PLAIN, height: int = 0):
        self.land = land
        self.waterValue = 1024 if land == LandType.FRESHWATER else 0
        self.grassValue = 1024 if land == LandType.GRASSLAND else 0
        self.height = height

class World:
    def __init__(self, width: int, length: int, layout: list[list[Cell]] = None):
        self.width = width
        self.length = length

        if layout:
            self.grid = layout
        else:
            # Random world generation
            raw = np.random.choice(
                [
                    Cell(land=LandType.PLAIN, height=0),
                    Cell(land=LandType.MOUNTAIN, height=256),
                    Cell(land=LandType.FRESHWATER, height=0),
                    Cell(land=LandType.GRASSLAND, height=0),
                ],
                size=(self.length, self.width)
            )
            # Convert to object array so each entry is a Cell instance
            self.grid = raw.tolist()

        # Calculate Distance from Freshwater
        dist = np.full((self.length, self.width), float("inf"))
        queue = deque()

        for l in range(self.length):
            for w in range(self.width):
                if self.grid[l][w].land == LandType.FRESHWATER:
                    dist[l][w] = 0
                    queue.append((l, w))

        # BFS to calculate Distance
        while queue:
            l, w = queue.popleft()
            for dl, dw in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nl, nw = l + dl, w + dw
                if 0 <= nl < self.length and 0 <= nw < self.width:
                    if dist[nl][nw] > dist[l][w] + 1 and self.grid[nl][nw].land != LandType.MOUNTAIN:
                        dist[nl][nw] = dist[l][w] + 1
                        queue.append((nl, nw))

        # Update water value
        for y in range(self.length):
            for x in range(self.width):
                cell = self.grid[y][x]
                if cell.land != LandType.MOUNTAIN:
                    d = dist[y][x]
                    cell.waterValue = int(1024 / (2 ** d)) if d != float('inf') else 0

    def get_cell(self, row, col) -> Cell:
        '''
        :param row: the row number
        :param col: the column number
        :return: the cell at the given position
        '''
        return self.grid[row][col]

    def update(self):
        '''
        Update all cells in the world with the given rules:

            Mountains will not get updated

            Freshwater will not get updated

            The water amount of each cell is the 1024 / (2^d) where d is distance to the nearest Freshwater

            Grassland will expend to neighbouring Plain cells

            If a cell is Grassland, it will double each update, however, if the water amount of that cell is less than
            the grass amount, it will be halved.

        The distance of two cells is the Euclidean distance between the two cells, however, if there is a mountain
        cell in between the two cells, the distance calculation has to go around the mountain cell.
        '''
        grass_positions = [
            (l, w)
            for l in range(self.length)
            for w in range(self.width)
            if self.grid[l][w].land == LandType.GRASSLAND
        ]

        # Grow or shrink grass
        for l, w in grass_positions:
            cell = self.grid[l][w]
            if cell.waterValue >= cell.grassValue:
                cell.grassValue *= 2
            else:
                cell.grassValue //= 2
            if cell.grassValue == 0:
                cell.land = LandType.PLAIN

        living_grass = [
            (l, w)
            for l in range(self.length)
            for w in range(self.width)
                if self.grid[l][w].land == LandType.GRASSLAND
        ]

        # Spread to neighboring plain cells
        for l, w in living_grass:
            for dl, dw in ((-1,0),(1,0),(0,-1),(0,1)):
                nl, nw = l + dl, w + dw
                if 0 <= nl < self.length and 0 <= nw < self.width:
                    neighbor = self.grid[nl][nw]
                    if neighbor.land == LandType.PLAIN:
                        neighbor.land = LandType.GRASSLAND
                        neighbor.grassValue = 1
