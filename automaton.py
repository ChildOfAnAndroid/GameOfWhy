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
        self.grid = environments.grid

    def runLoop(self, turn):
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                cell = self.grid[x,y]
                if isinstance(cell, Cell):
                    if cell.step_count < turn:
                        cell.step_count = turn
                        cell.move(grid, lightGrid, inertGrid)
                        cell.absorb_nutrients(lightGrid)
                        cell.phase_transition()
                        cell.reproduce(grid, lightGrid)
                        cell.decay(lightGrid, inertGrid)
                        cell.waifuSignal(waifuGrid)
                        if cell.energy > top_energy:
                            top_energy = cell.energy
        
    for _ in range(CELL_BASE_COUNT):
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        organism = Organism(next_organism_id)
        next_organism_id += 1
        new_cell = Cell(x, y, stats, organism=organism)
        new_cell.role = random.choice(CELL_ROLES)
        #new_cell.state = cell.state if random.random() < .001 else False #random.choice([True, False])
        cells.append(new_cell)
        organism.add_cell(new_cell)
        organisms.append(organism)
        grid[x, y] = new_cell



    enrich_environment(lightGrid, waifuGrid, inertGrid)  # Replenish nutrients dynamically
        
    #if step % 100 == 0:  # Stir the environment every 100 steps
    #    stir_environment(grid)

    stats.endTurn()

    print(stats)