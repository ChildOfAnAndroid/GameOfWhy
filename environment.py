# ENVIRONMENT FILE: GAME OF WHY
# CHARIS CAT 2024

import numpy as np
import random

class Environment:
    # Create grid and environment
    def environmentGeneration():
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=object)  # Allow tracking cell states
    lightGrid = np.random.random((GRID_SIZE, GRID_SIZE)) * 5  # Light levels
    waifuGrid = np.zeros((GRID_SIZE, GRID_SIZE))
    inertGrid = np.zeros((GRID_SIZE, GRID_SIZE)) # Fully decayed inerts

    # Enrich environment dynamically
    def enrich_environment(lightGrid, waifuGrid, inertGrid):
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

    def stir_environment(grid):
        # Randomly displace cells to "stir things up"
        for _ in range(100):  # Number of cells to displace
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            if isinstance(grid[x, y], Cell):
                dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
                new_x = (x + dx) % GRID_SIZE
                new_y = (y + dy) % GRID_SIZE
                if grid[new_x, new_y] is None:
                    grid[new_x, new_y].stats.addCellMove()
                    grid[new_x, new_y] = grid[x, y]
                    grid[x, y] = None
                            
    print("Done with env")