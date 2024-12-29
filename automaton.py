# AUTOMATON SIMULATION FILE: GAME OF WHY
# CHARIS CAT 2024

import numpy as np
import random
from config import *
from cell import *

# Automaton manages the Cells & Organisms
class Automaton:
    def __init__(self, stats, environments):
        self.cells = []
        self.stats = stats
        self.environments = environments

        self.initialize()

    def initialize(self):
        for _ in range(CELL_BASE_COUNT):
            x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
            organism = None # Organism(next_organism_id)
            # next_organism_id += 1
            new_cell = Cell(x, y, self.stats, self.environments, organismCheck=organism)
            new_cell.role = random.choice(CELL_ROLES)
            #new_cell.state = cell.state if random.random() < .001 else False #random.choice([True, False])
            self.cells.append(new_cell)
            # organism.add_cell(new_cell)
            # organisms.append(organism)
            self.environments.grid[x, y] = new_cell

    def runLoop(self, turn):
        for x in range(self.environments.grid.shape[0]):
            for y in range(self.environments.grid.shape[1]):
                cell = self.environments.grid[x,y]
                if isinstance(cell, Cell):
                    if cell.needTurn(turn):
                        cell.runLoop(turn)
