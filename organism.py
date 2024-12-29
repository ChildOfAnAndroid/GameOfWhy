# ORGANISM CLASS FILE: GAME OF WHY
# CHARIS CAT 2024

import numpy as np
import random

class Organism:
    def __init__(self, organism_id):
        self.organism_id = organism_id
        self.cells = []  # List of cells belonging to this organism
        self.name = None  # Organisms can develop names
        self.reproduction_method = "asexual"  # Default reproduction method

    def add_cell(self, cell):
        self.cells.append(cell)

    def is_alive(self):
        return any(cell.alive for cell in self.cells)

    def fitness(self):
        # Fitness score based on energy, number of cells, and average traits
        if not self.is_alive():
            return 0
        total_energy = sum(cell.energy for cell in self.cells if cell.alive)
        avg_resilience = np.mean([cell.resilience for cell in self.cells if cell.alive])
        return total_energy * avg_resilience * len(self.cells)

    def center_of_mass(self):
        x = np.mean([cell.x for cell in self.cells if cell.alive])
        y = np.mean([cell.y for cell in self.cells if cell.alive])
        return int(x), int(y)

    def evolve_reproduction(self):
        if random.random() < self.mutation_rate:
            self.reproduction_method = random.choice(["asexual", "budding", "fragmentation", "spawning"])
    
    def attempt_sentience(self):
        if len(self.cells) > 3 and random.random() < 0.01:  # Random chance for large organisms
            self.name = "Entity_" + str(self.organism_id)

# Simulation parameters
organisms = []
next_organism_id = 1

"""
    new_organisms = []
    for organism in organisms:
        for cell in organism.cells:
            cell.move(grid, lightGrid)
            cell.absorb_nutrients(lightGrid)
            cell.phase_transition(lightGrid)
            baby = cell.reproduce(organism, grid, lightGrid)
            if baby:
                new_organisms.append(baby)
            cell.decay(lightGrid)

    organisms.extend(new_organisms)
    organisms = [org for org in organisms if org.is_alive()]
    """