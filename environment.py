# ENVIRONMENT FILE: GAME OF WHY
# CHARIS CAT 2024

# from scipy.ndimage import gaussian_filter
import numpy as np
import random
from config import *
from cell import *

# Environment manages the environments
class Environment:
    # Create grid and environment
    def __init__(self, stats):
        self.stats = stats
        self.grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=object)  # Allow tracking cell states
        self.lightGrid = np.ones((GRID_SIZE, GRID_SIZE)) * 10  # Light levels
        self.waifuGrid = np.zeros((GRID_SIZE, GRID_SIZE))
        self.inertGrid = np.zeros((GRID_SIZE, GRID_SIZE)) # Fully decayed inerts
        self.signalGrid = np.zeros((GRID_SIZE, GRID_SIZE))  # Shared perception map

    def updateSignalGrid(self):
        self.signalGrid.fill(0)
        # Combine light, waifu, and grid contents
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                cell = self.grid[x, y]

                # Base signal from light and waifu grids
                baseSignal = (self.lightGrid[x, y] * LIGHT_GRID_IMPORTANCE) + (self.waifuGrid[x, y] * ATTRACTIVENESS_GRID_IMPORTANCE) + (self.inertGrid[x, y] * INERT_GRID_IMPORTANCE)

                if cell is None or cell == 0 or cell == "gas":
                    # Empty or passable space, keep base signal
                    self.signalGrid[x, y] = baseSignal
                elif isinstance(cell, Cell):
                    # Occupied by a cell: factor in cell attributes
                    cellSignal = baseSignal
                    cellSignal -= cell.resilience * 0.1
                    if cell.state == "liquid":
                        cellSignal += random.uniform(0.5,2)
                    cellSignal += cell.lightEmission * 1.2
                    self.signalGrid[x, y] = cellSignal
                else:
                    # Impassable terrain (e.g., "inert"), zero out the signal
                    self.signalGrid[x, y] = baseSignal * 0.01

    # Enrich environment dynamically
    def enrich_environment(self):
        # Brighten some random areas
        for _ in range(ENVIRONMENT_LIGHT_ENRICHMENT_SOURCE_NUM):  # Number of light sources
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            self.lightGrid[x, y] = min((self.lightGrid[x, y] + ENVIRONMENT_LIGHT_ENRICHMENT), ENVIRONMENT_LIGHT_CLIP_MAX)  # Cap at max brightness
        self.lightGrid -= random.uniform(-0.5, 1.5) * LIGHT_GRID_DECAY_RATE
        self.lightGrid = np.clip(self.lightGrid, ENVIRONMENT_LIGHT_CLIP_MIN, ENVIRONMENT_LIGHT_CLIP_MAX)
        self.waifuGrid -= ATTRACTIVENESS_GRID_DECAY_RATE
        self.inertGrid -= INERT_GRID_DECAY_RATE
        #print(lightGrid)
        #print(np.min(lightGrid))
        #print(np.max(lightGrid))
        #lightGrid = gaussian_filter(lightGrid, sigma=1)  # sigma = more/less blur
        #print(lightGrid)

    def stir_environment(self, grid):
        # Randomly displace cells to "stir things up"
        for _ in range(100):  # Number of cells to displace
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if isinstance(grid[x, y], Cell):
                dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                new_x = (x + dx) % GRID_SIZE
                new_y = (y + dy) % GRID_SIZE
                if grid[new_x, new_y] is None:
                    self.stats.addCellMove()
                    grid[new_x, new_y] = grid[x, y]
                    grid[x, y] = None
    
    def runLoop(self, turn):
        self.updateSignalGrid()
        self.enrich_environment()
        if turn % 100 == 0 and False: # disabled for now
            self.stir_environment()

    def _boundXY(self, coords):
        x, y = coords
        return x % self.grid.shape[0], y % self.grid.shape[1]

    def attemptForcedSpawn(self, coords):
        x, y = self._boundXY(coords)
        if self.grid[x, y] == 0 or self.grid[x, y] is None:
            self.stats.addCellForcedSpawn()
            new_cell = Cell(x, y, self.stats, self, organismCheck=None)
            new_cell.role = random.choice(CELL_ROLES)
            self.grid[x, y] = new_cell
            print(f"Placed a {new_cell.role} cell at ({x}, {y})")
        else:
            self.stats.addCellFailedForcedSpawn()
            print(f"Failed placing a new cell, cell ({x} {y}) is full")

    # Get light amount at a coordinate
    def getLightAt(self, x, y):
        x, y = self._boundXY((x, y))
        return self.lightGrid[x, y]
    
    # Change light amount at a coordinate by an arbitrarty amount while ensuring bounds
    def setLightAt(self, x, y, value):
        x, y = self._boundXY((x, y))
        self.lightGrid[x, y] = min(ENVIRONMENT_LIGHT_CLIP_MAX, max(ENVIRONMENT_LIGHT_CLIP_MIN, value))
        return self.lightGrid[x, y] > 0
    
    def addLightAt(self, x, y, amount):
        return self.setLightAt(x, y, self.getLightAt(x, y) + amount)

    def depleteLightAt(self, x, y, amount):
        return self.addLightAt(x, y, amount * -1)
    
    def getAttractivenessAt(self, x, y):
        x, y = self._boundXY((x, y))
        return self.waifuGrid[x, y]
    
    def addAttractivenessAt(self, x, y, amount):
        return self.setAttractivenessAt(x, y, self.getAttractivenessAt(x, y) + amount)
    
    def setAttractivenessAt(self, x, y, value):
        x, y = self._boundXY((x, y))
        self.waifuGrid[x, y] = min(ENVIRONMENT_ATTRACTIVENESS_CLIP_MAX, max(ENVIRONMENT_ATTRACTIVENESS_CLIP_MIN, value))
        return self.waifuGrid[x, y] > 0
    
    def getInertAt(self, x, y):
        x, y = self._boundXY((x, y))
        return self.inertGrid[x, y]
    
    def addInertAt(self, x, y, amount):
        return self.setInertAt(x, y, self.getInertAt(x, y) + amount)
    
    def depleteInertAt(self, x, y, amount):
        return self.addInertAt(x, y, amount * -1)

    def setInertAt(self, x, y, value):
        x, y = self._boundXY((x, y))
        self.inertGrid[x, y] = value
        return self.inertGrid[x, y] > 0
    
    def getCellsAt(self, x, y):
        x, y = self._boundXY((x, y))
        return [self.grid[x, y]]
        # return self.grid[x, y]

    def getCellAt(self, x, y):
        x, y = self._boundXY((x, y))
        return self.grid[x, y]
    
    def setCellAt(self, x, y, cell):
        x, y = self._boundXY((x, y))
        self.grid[x, y] = cell

    def moveCellTo(self, x, y, cell):
        x, y = self._boundXY((x, y))
        self.grid[cell.x, cell.y] = None
        self.grid[x, y] = cell
        cell.x = x
        cell.y = y

    def removeCellAt(self, x, y, cell):
        if self.getCellAt(x, y) == cell:
            self.setCellAt(x, y, None)
        else:
            raise Exception("The cell {cell} isn't located here and can't be removed")

    def removeCellFromGrid(self, cell):
        self.removeCellAt(cell.x, cell.y, cell)

    def canAddCellAt(self, x, y):
        x, y = self._boundXY((x, y))
        return self.grid[x, y] is None or self.grid[x, y] == 0
        # len(self.grid[x, y]) == 0 or (len(self.grid[x, y]) == 1 and self.grid[x, y][0].state == "gas")
