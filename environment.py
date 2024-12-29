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
        self.lightGrid = np.random.random((GRID_SIZE, GRID_SIZE)) * 5  # Light levels
        self.waifuGrid = np.zeros((GRID_SIZE, GRID_SIZE))
        self.inertGrid = np.zeros((GRID_SIZE, GRID_SIZE)) # Fully decayed inerts

    # Enrich environment dynamically
    def enrich_environment(self, lightGrid, waifuGrid, inertGrid):
        # Brighten some random areas
        for _ in range(ENVIRONMENT_LIGHT_ENRICHMENT_SOURCE_NUM):  # Number of light sources
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            lightGrid[x, y] = min(lightGrid[x, y] + ENVIRONMENT_LIGHT_ENRICHMENT, ENVIRONMENT_LIGHT_CLIP_MAX)  # Cap at max brightness
        lightGrid -= LIGHT_GRID_DECAY_RATE
        lightGrid = np.clip(lightGrid, ENVIRONMENT_LIGHT_CLIP_MIN, ENVIRONMENT_LIGHT_CLIP_MAX)
        waifuGrid -= ATTRACTIVENESS_GRID_DECAY_RATE
        inertGrid -= INERT_GRID_DECAY_RATE
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
        self.enrich_environment()
        if turn % 100 == 0 and False: # disabled for now
            self.stir_environment()

    def attemptForcedSpawn(self, coords):
        x, y = coords
        if self.grid[x, y] == 0 or self.grid[x, y] is None:
            self.stats.addCellForcedSpawn()
            new_cell = Cell(x, y, self.stats, organism=None)
            new_cell.role = random.choice(CELL_ROLES)
            self.grid[x, y] = new_cell
            print(f"Placed a {new_cell.role} cell at ({x}, {y})")
        else:
            self.stats.addCellFailedForcedSpawn()
            print(f"Failed placing a new cell, cell ({x} {y}) is full")

    # Get light amount at a coordinate
    def getLightAt(self, x, y):
        return self.lightGrid[x, y]
    
    # Change light amount at a coordinate by an arbitrarty amount while ensuring bounds
    def setLightAt(self, x, y, value):
        self.lightGrid[x, y] = min(ENVIRONMENT_LIGHT_CLIP_MAX, max(ENVIRONMENT_LIGHT_CLIP_MIN, value))
        return self.lightGrid[x, y] > 0
    
    def addLightAt(self, x, y, amount):
        return self.setLightAt(x, y, self.getLightAt(x, y) + amount)

    def depleteLightAt(self, x, y, amount):
        return self.addLightAt(x, y, amount * -1)
    
    def getAttractivenessAt(self, x, y):
        return self.waifuGrid[x, y]
    
    def addAttractivenessAt(self, x, y, amount):
        return self.setAttractivenessAt(x, y, self.getAttractivenessAt(x, y) + amount)
    
    def setAttractivenessAt(self, x, y, value):
        self.waifuGrid = min(ENVIRONMENT_ATTRACTIVENESS_CLIP_MAX, max(ENVIRONMENT_ATTRACTIVENESS_CLIP_MIN, value))
        return self.waifuGrid[x, y] > 0
    
    def getInertAt(self, x, y):
        return self.inertGrid[x, y]
    
    def addInertAt(self, x, y, amount):
        return self.setInertAt(x, y, self.getInertAt(x, y) + amount)
    
    def depleteInertAt(self, x, y, amount):
        return self.addInertAt(x, y, amount * -1)

    def setInertAt(self, x, y, value):
        self.inertGrid[x, y] = value
        return self.inertGrid[x, y] > 0