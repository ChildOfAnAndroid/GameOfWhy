# MAIN FILE: GAME OF WHY
# CHARIS CAT 2024

import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.patches as mpatches
from matplotlib.colors import hsv_to_rgb
from functools import partial
from scipy.ndimage import gaussian_filter
from matplotlib.colors import LinearSegmentedColormap
from config import *

class Stats:
    def __init__(self):
        # Population
        self.cellCounter = 0

        # death statistics
        self.cellDeathCounter = {}
        self.cellDeathEscapeCounter = 0

        # birth statistics
        self.cellBabyCounter = 0
        self.cellBabysFailedCounter = 0

        # Movement statistics
        self.cellMovedCounter = 0
        self.cellPushedCounter = 0

        # TURN STATISTICS
        self.cellBabysThisTurn = 0
        self.cellBabysFailedThisTurn = 0
        self.cellDeathsThisTurn = {}
        self.cellDeathEscapesThisTurn = 0
        self.cellMovedThisTurn = 0
        self.cellPushedThisTurn = 0
        self.cellAliveCount = 0

    def beginTurn(self):
        self.cellBabysThisTurn = 0
        self.cellDeathsThisTurn = {}
        self.cellDeathEscapesThisTurn = 0
        self.cellBabysFailedThisTurn = 0
        self.cellAliveCount = 0
        self.cellPushedThisTurn = 0
        self.cellMovedThisTurn = 0

    def endTurn(self):
        print(f"Turn Summary: There are currently {self.cellAliveCount} living cells. There were {self.cellBabysThisTurn} babies born, {self.getDeathsThisTurn()} cells died, and {self.cellDeathEscapesThisTurn} cells evaded death! ")
        print(self)

    def __str__(self):
        return f"""
Total Cell Count: {self.cellCounter+1}

# Death Statistics
Total Cell Death: {self.getTotalDeath()}
By Reason:
{"\n".join([f"{x}: {self.cellDeathCounter[x]}" for x in self.cellDeathCounter])}
Total Cell Escapes: {self.cellDeathEscapeCounter}

# Birth Statistics
Total Cell Babies: {self.cellBabyCounter}
Total Cell Skipped Babies: {self.cellBabysFailedCounter}

# Movement Statistics
Total Cell Movements: {self.cellMovedCounter}
Total Cell Pushed: {self.cellPushedCounter}

# Turn Statistics
Cell Babies: {self.cellBabysThisTurn}
Cell Skipped Babies: {self.cellBabysFailedThisTurn}
Cell Death: {self.getDeathsThisTurn()}
{"\n".join([f"{x}: {self.cellDeathsThisTurn[x]}" for x in self.cellDeathsThisTurn])}
Cell Escapes: {self.cellDeathEscapesThisTurn}
Cell Movements: {self.cellMovedThisTurn}
Cell Pushes: {self.cellPushedThisTurn}
Cells Alive: {self.cellAliveCount}
"""

    def addCellBaby(self):
        self.cellBabyCounter += 1
        self.cellBabysThisTurn += 1
    
    def addCellBabyFailed(self):
        self.cellBabysFailedCounter += 1
        self.cellBabysFailedThisTurn += 1
    
    def addCellDeath(self, reason):
        if reason in self.cellDeathCounter:
            self.cellDeathCounter[reason] += 1
        else:
            self.cellDeathCounter[reason] = 1
        
        if reason in self.cellDeathsThisTurn:
            self.cellDeathsThisTurn[reason] += 1
        else:
            self.cellDeathsThisTurn[reason] = 1

    def addCellDeathEscape(self):
        self.cellDeathEscapeCounter += 1
        self.cellDeathEscapesThisTurn += 1

    def addCellPush(self):
        self.cellPushedCounter += 1
        self.cellPushedThisTurn += 1
    
    def addCellAlive(self):
        self.cellAliveCount += 1

    def addCellMove(self):
        self.cellMovedCounter += 1
        self.cellMovedThisTurn += 1

    def getTotalDeath(self):
        total = 0
        for reason in self.cellDeathCounter:
            total += self.cellDeathCounter[reason]
        return total

    def getDeathsThisTurn(self):
        sum = 0
        for reason in self.cellDeathsThisTurn:
            sum += self.cellDeathsThisTurn[reason]
        return sum

    def getCellNextID(self):
        ret = self.cellCounter
        self.cellCounter += 1
        return ret

class Cell:
    def __init__(self, x, y, stats, organism=None):
        self.id = stats.getCellNextID()
        self.step_count = 0
        self.x = x
        self.y = y
        self.energy = random.uniform(CELL_BASE_ENERGY_MIN, CELL_BASE_ENERGY_MAX)  # Starting energy level
        self.age = 0  # Age of the cell
        self.mutation_rate = CELL_BASE_MUTATION_RATE_MIN  # Probability of mutation during reproduction
        self.alive = True
        self.role = "general"  # Role of the cell: general, structural, sensory, reproductive
        self.growth_rate = random.uniform(CELL_BASE_GROWTH_RATE_MIN, CELL_BASE_GROWTH_RATE_MAX)  # Genetic trait for energy absorption
        self.resilience = random.uniform(CELL_BASE_RESILIENCE_MIN, CELL_BASE_RESILIENCE_MAX)  # Resistance to harsh environments
        self.perception_strength = random.uniform(CELL_BASE_PERCEPTION_MIN, CELL_BASE_PERCEPTION_MIN)  # Communication ability
        self.speed = random.uniform(CELL_BASE_SPEED_MIN, CELL_BASE_SPEED_MAX)  # Speed of movement
        self.phase_transition() # Call to set cell state & color
        self.light_emission = CELL_BASE_LIGHT_EMISSION_MIN  # Amount of light emitted (e.g., by plasma or bioluminescence)
        self.light_absorption = random.uniform(CELL_BASE_LIGHT_ABSORPTION_MIN, CELL_BASE_LIGHT_ABSORPTION_MAX)  # Ability to absorb light
        self.attractiveness = CELL_BASE_ATTRACTIVENESS_MIN
        self.genome = {
            'growth_rate': self.growth_rate,
            'resilience': self.resilience,
            'perception_strength': self.perception_strength,
            'speed': self.speed,
            'role': self.role
        }
        self.organism = organism  # Tracks which organism this cell belongs to
        self.stats = stats
        


    def move_or_squish(self, moving, direction, grid, inertGrid):
        dx, dy = direction
        new_x = (self.x + dx) % grid.shape[0]
        new_y = (self.y + dy) % grid.shape[1]
        # Found an empty space
        if grid[new_x, new_y] == 0 or grid[new_x, new_y] is None:
            grid[self.x, self.y] = None
            self.x = new_x
            self.y = new_y
            grid[self.x, self.y] = self
            print(f"Escaped a death squish!")
            self.stats.addCellDeathEscape()
            self.stats.addCellMove()
            if not self.alive: # if cell is already inert and needs to move, update inertGrid
                inertGrid[self.x, self.y] += 300
            return True
        else:
            if isinstance(grid[new_x, new_y], Cell):
                if grid[new_x, new_y].resilience > grid[self.x,self.y].resilience:
                    # the target cell get squished
                    ratio = random.uniform(CELL_DEATH_RELEASE_SQUISH_MIN, CELL_DEATH_RELEASE_SQUISH_MAX)
                    grid[new_x, new_y].energy += max(0, self.energy * ratio) # Squish release of energy (norty?!)
                    moving.energy += max(0, self.energy * (1-ratio))
                    self.alive = False
                    grid[self.x, self.y] = None
                    print(f"Died from cuddles. Energy: {self.energy}, lost {(1 / self.resilience) * self.speed} this turn {self}")
                    self.stats.addCellDeath(CELL_DEATH_REASON_SQUISH)
                    inertGrid[self.x, self.y] += CELL_DEATH_RELEASE_INERT
                    return False
                else:
                    # the destination cell moves out the way
                    grid[new_x, new_y].move_or_squish(self, direction, grid, inertGrid)
                    grid[self.x, self.y] = None
                    self.x, self.y = (new_x, new_y)
                    grid[self.x, self.y] = self
                    print(f"The Vengabus is Evolving O.o")
                    self.stats.addCellPush()
                    self.stats.addCellMove()
                    if not self.alive:
                        inertGrid[self.x, self.y] += CELL_DEATH_RELEASE_INERT
                    
            else:
                print(f"IDK WHAT'S HERE: {grid[new_x, new_y]}")
        return True
        
    def move(self, grid, lightGrid, inertGrid):
        if not self.alive or self.energy < CELL_MOVE_ENERGY_MIN:
            # print(f"Not moving because alive is {self.alive} & energy is {self.energy}")
            return
        # Movement based on environmental signals and nutrient concentration
        potential_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(potential_moves)
        best_move = (0, 0)
        max_signal = -1
        for dx, dy in potential_moves:
            # print(f"Considering move ({dx},{dy})")
            new_x = (self.x + dx) % grid.shape[0]
            new_y = (self.y + dy) % grid.shape[1]
            if grid[new_x, new_y] == 0 or grid[new_x, new_y] is None or grid[new_x, new_y] == "gas":  # Allow passage through gas
                # print(f"Space is empty signal is {abs(lightGrid[new_x, new_y])} * {self.perception_strength}, max_signal is currently {max_signal}")
                # TODO: change that to having "moving towards the highest energy cell it can sense"
                signal = (abs(lightGrid[new_x, new_y]) * (waifuGrid[new_x, new_y]) * self.perception_strength) * ENVIRONMENT_VISIBILITY_MULTIPLIER
                # print(f"env: {lightGrid[new_x, new_y]} wai: {waifuGrid[new_x, new_y]} per: {self.perception_strength}")
                if signal > max_signal:
                    # print(f"Best signal")
                    best_move = (dx, dy)
                    max_signal = signal
            elif self.resilience > grid[new_x,new_y].resilience:
                # Current cell resilience sup to target resilience
                # Try to push the target away
                # print(f"Squish time")
                grid[new_x,new_y].move_or_squish(self, (dx, dy), grid, inertGrid)
                best_move = (dx, dy)
                break
            # else:
            #    print(f"Space is full")

        dx, dy = best_move
        new_x = (self.x + dx) % grid.shape[0]
        new_y = (self.y + dy) % grid.shape[1]
        blockCounter = 0
        if grid[new_x, new_y] == 0 or grid[new_x, new_y] is None or grid[new_x, new_y] == "gas" and blockCounter == 0:  # Move if space is empty or gas
            # print(f"Moving {self.id} from ({self.x}, {self.y}) to ({new_x}, {new_y})")
            grid[self.x, self.y] = None
            self.x, self.y = new_x, new_y
            grid[self.x, self.y] = self
            self.stats.addCellMove()
        else:
            if (dx, dy) == (0, 1) and blockCounter < 4:
                dx, dy = (1, 0)
                # print(f"Blocked, attempting to move to {new_x, new_y}")
                blockCounter += 1
                grid[self.x, self.y] = None
                self.x, self.y = (self.x + dx) % grid.shape[0], (self.y + dy) % grid.shape[1]
                grid[self.x, self.y] = self
                self.stats.addCellMove()
            if (dx, dy) == (1, 0) and blockCounter < 4:
                dx, dy = (0, -1)
                # print(f"Blocked, attempting to move to {new_x, new_y}")
                blockCounter += 1
                grid[self.x, self.y] = None
                self.x, self.y = (self.x + dx) % grid.shape[0], (self.y + dy) % grid.shape[1]
                grid[self.x, self.y] = self
                self.stats.addCellMove()
            if (dx, dy) == (0, -1) and blockCounter < 4:
                dx, dy = (-1, 0)
                # print(f"Blocked, attempting to move to {new_x, new_y}")
                blockCounter += 1
                grid[self.x, self.y] = None
                self.x, self.y = (self.x + dx) % grid.shape[0], (self.y + dy) % grid.shape[1]
                grid[self.x, self.y] = self
                self.stats.addCellMove()
            if (dx, dy) == (-1, 0) and blockCounter < 4:
                dx, dy = (0, 1)
                # print(f"Blocked, attempting to move to {new_x, new_y}")
                blockCounter += 1
                grid[self.x, self.y] = None
                self.x, self.y = (self.x + dx) % grid.shape[0], (self.y + dy) % grid.shape[1]
                grid[self.x, self.y] = self
                self.stats.addCellMove()
            else:
                if self.x != new_x or self.y != new_y:
                    print(f"Failed moving {self.id} from ({self.x}, {self.y}) to ({new_x}, {new_y})")
                else:
                    print(f"Failed moving {self.id} onto itself")
        
    def get_color(self, top_energy):
        if self.organism:
            if self.organism.name: # sentient = random color picked once
                if not hasattr(self.organism, "color"):
                    self.organism.color = hsv_to_rgb((random.uniform(0, 1), min(1, max(0.8, self.energy / top_energy)), min(max(0.5, self.energy / top_energy), 1)))
                    return self.organism.color
            else: # dark blue
                return hsv_to_rgb((0.6, min(1, max(0.8, self.energy / top_energy)), min(1, max(0.8, self.energy / top_energy))))
        if not self.alive:
            return hsv_to_rgb((self.hue, 1, 0.2))
        else:
            return hsv_to_rgb((self.hue, min(1, max(0.5, self.energy / (top_energy))), min(1, max(0.8, self.energy / top_energy))))

    def get_alpha(self):
        if cell.state == "gas":
            return 0.3
        return 1

    def absorb_nutrients(self, lightGrid):
        if self.alive:
            nutrients = lightGrid[self.x, self.y]
            self.energy += nutrients * self.growth_rate * 5
            lightGrid[self.x, self.y] = max(lightGrid[self.x, self.y] - 0.02, 0)  # Deplete nutrients

    def emit_light(self, lightGrid):
        if self.state == "plasma": # Plasma cells consistently emit high light
            self.light_emission = 5
            lightGrid[self.x, self.y] = min(lightGrid[self.x, self.y] + self.light_emission, 100)
        elif random.random() < 0.01 and self.energy > 120: # Non-plasma cells have a random chance to emit light
            self.light_emission = 1
            lightGrid[self.x, self.y] = min(lightGrid[self.x, self.y] + self.light_emission, 100)
        else:
            self.light_emission = 0
            
    def waifuSignal(self, waifuGrid):
        if self.alive:
            waifuGrid[self.x, self.y] = min(waifuGrid[self.x, self.y] + self.attractiveness, 100)
            vibes = waifuGrid[self.x, self.y]
            self.attractiveness += vibes * self.growth_rate * 0.5
        else:
            waifuGrid[self.x, self.y] = 0

    def sense_environment(self, grid):
        if not self.alive:
            return None
        # Detect neighboring states and light levels
        neighbor_states = {}
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = (self.x + dx) % grid.shape[0], (self.y + dy) % grid.shape[1]
            neighbor_states[(dx, dy)] = {
                "state": grid[nx, ny],
                "light": grid[nx, ny].light_emission if isinstance(grid[nx, ny], Cell) else 0,
                "rating": grid[nx, ny].waifuSignal if isinstance(grid[nx, ny], Cell) else 0
            }
        return neighbor_states
        # print(neighbor_states)
            
    # State of the cell: solid, liquid, gas, plasma, inert
    def phase_transition(self):
        if self.energy > CELL_STATE_PLASMA_ENERGY:
            self.state = "plasma"
            self.hue = random.uniform(CELL_STATE_PLASMA_COLOR_MIN, CELL_STATE_PLASMA_COLOR_MAX)
        elif CELL_STATE_GAS_ENERGY < self.energy <= CELL_STATE_PLASMA_ENERGY:
            self.state = "gas"
            self.hue = random.uniform(CELL_STATE_GAS_COLOR_MIN, CELL_STATE_GAS_COLOR_MAX)
        elif CELL_STATE_LIQUID_ENERGY < self.energy <= CELL_STATE_GAS_ENERGY:
            self.state = "liquid"
            self.hue = random.uniform(CELL_STATE_LIQUID_COLOR_MIN, CELL_STATE_LIQUID_COLOR_MAX)
        elif CELL_STATE_SOLID_ENERGY < self.energy <= CELL_STATE_LIQUID_ENERGY:
            self.state = "solid"
            self.hue = random.uniform(CELL_STATE_SOLID_COLOR_MIN, CELL_STATE_SOLID_COLOR_MAX)
        elif CELL_STATE_INERT_ENERGY < self.energy <= CELL_STATE_SOLID_ENERGY:
            self.state = "inert"
            self.hue = self.hue if hasattr(self, "hue") else random.uniform(CELL_STATE_INERT_COLOR_MIN, CELL_STATE_INERT_COLOR_MAX)

    def reproduce(self, grid, lightGrid):
        if not self.alive or (self.age > CELL_FERTILITY_AGE_MAX) or (self.age < CELL_FERTILITY_AGE_MIN):
            return False
        # reproducing a cell inside an organism (will be done in organism)
        #if self.organism is not None:
        #    return
        # Generate a baby cell if enough energy
        if random.random() < CELL_FERTILITY_CHANCE_MIN or self.attractiveness > 9 or self.energy > CELL_FERTILITY_ENERGY_MIN:
            x, y = (cell.x + random.choice([-1, 1])) % grid.shape[0], (cell.y + random.choice([-1, 1])) % grid.shape[1]
            if grid[x, y] == 0 or grid[x, y] is None:  # Empty spot
                self.energy = (self.energy/CELL_REPRODUCTION_SUCCESS_COST)
                baby_cell = Cell(x, y, self.stats, organism=None)
                baby_cell.growth_rate = max(0.5, min(2.0, cell.growth_rate + random.uniform(CELL_BABY_MUTATION_GROWTH_MIN, CELL_BABY_MUTATION_GROWTH_MAX)))
                baby_cell.resilience = max(0.5, min(2.0, cell.resilience + random.uniform(CELL_BABY_MUTATION_RESILIENCE_MIN, CELL_BABY_MUTATION_RESILIENCE_MAX)))
                baby_cell.perception_strength = max(0.1, min(1.0, cell.perception_strength + random.uniform(CELL_BABY_MUTATION_PERCEPTION_MIN, CELL_BABY_MUTATION_PERCEPTION_MAX)))
                baby_cell.speed = max(0.5, min(2.0, cell.speed + random.uniform(CELL_BABY_MUTATION_SPEED_MIN, CELL_BABY_MUTATION_SPEED_MAX)))
                baby_cell.role = random.choice(CELL_ROLES)
                grid[x, y] = baby_cell
                # print("UNEBEBEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!!!!!!1!!!!!!!!!!!!!1!!!")
                self.stats.addCellBaby()
                return True
            else:
                self.energy = (self.energy/CELL_REPRODUCTION_FAILURE_COST)
                # print("Tried to UNEBEBEBEBEBEBEBEE BUT NO SPACE LEFT")
                self.stats.addCellBabyFailed()
                return False
        return False

    def decay(self, lightGrid, inertGrid):
        if not self.alive:
            return
        self.energy -= (CELL_DECAY_ENERGY_MULTIPLIER / (self.resilience+(self.age/100)) * self.speed)  # Energy loss increases with speed
        self.age += CELL_DECAY_AGE_PER_TURN
        self.attractiveness = ((self.energy*(CELL_ATTRACTIVENESS_NORM_ENERGY/100))+(self.age*(CELL_ATTRACTIVENESS_NORM_AGE/100))+(self.growth_rate*CELL_ATTRACTIVENESS_NORM_GROWTH)+(self.resilience*CELL_ATTRACTIVENESS_NORM_RESILIENCE)+(self.perception_strength*CELL_ATTRACTIVENESS_NORM_STRENGTH)+(self.speed*CELL_ATTRACTIVENESS_NORM_SPEED)+(self.light_emission*CELL_ATTRACTIVENESS_NORM_LIGHT_EMISSION))/70
        #print(f"Rated {self.attractiveness}% hot")
        if self.energy <= 0 or self.age > (self.resilience * random.uniform(CELL_DEATH_AGE_MIN, CELL_DEATH_AGE_MAX)):  # Death by starvation or old age
            self.alive = False
            print(f"Died from state {self.state} Energy: {self.energy}, lost {(1 / self.resilience) * self.speed} this turn")
            if self.energy >= 0:
                self.stats.addCellDeath(CELL_DEATH_REASON_AGE)
            else:
                self.stats.addCellDeath(CELL_DEATH_REASON_STARVATION)
            self.energy = 0
            self.state = "inert"
            lightGrid[self.x, self.y] += CELL_DEATH_RELEASE_LIGHT  # Dead cells release light for some reason
            inertGrid[self.x, self.y] += CELL_DEATH_RELEASE_INERT # Drop inert resources onto inert grid

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

# Create grid and environment
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


def on_click(stats, event):
    # Handles mouse clicks to place cells
    if event.xdata is None or event.ydata is None:
        return
    x, y = int(event.ydata), int(event.xdata)
    if grid[x, y] == 0 or grid[x, y] is None:
        new_cell = Cell(x, y, stats, organism=None)
        counter += 1
        new_cell.role = random.choice(CELL_ROLES)
        grid[x, y] = new_cell
        print(f"Placed a {new_cell.role} cell at ({x}, {y})")

cells = []
stats = Stats()
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

# Define RGBA colors for the gradient: transparent -> green -> brown
colors = [
    (0, 0, 0, 0),      # transparent
    (0.1, 0.3, 0.1, 1),  # green
    (0.4, 0.3, 0.2, 1),  # brown
    (0.2, 0.2, 0.2, 1)   # grey
]

# Create the colormap
terrain_colormap = LinearSegmentedColormap.from_list("terrain_colormap", colors)

colors = [
        (0.0, (1, 1, 1, 0)),
        (0.3, (0.5, 0.1, 0.5, 0.2)),
        (0.7, (1.0, 0.5, 0.0, 0.6)),
        (1.0, (1.0, 1.0, 0.0, 0.8)),
    ]
    
purple_yellow_colormap = LinearSegmentedColormap.from_list("purple_yellow", colors)


# Visualization and Interaction
plt.ion()
fig, ax = plt.subplots()
cid = fig.canvas.mpl_connect('button_press_event', partial(on_click, stats))
top_energy = VISUALISATION_BASE_ENERGY_TOP_RECORD
for step in range(NUM_STEPS):
    print(f"Step {step} start")
    stats.beginTurn()
    ax.clear()
    #ax.imshow(gridSize, alpha=0.5)
    ax.imshow(inertGrid, cmap=terrain_colormap, alpha=INERT_GRID_TRANSPARENCY)
    ax.imshow(waifuGrid, cmap="BuPu", alpha=ATTRACTIVENESS_GRID_TRANSPARENCY, interpolation="bilinear")
    ax.imshow(lightGrid, cmap=purple_yellow_colormap, alpha=LIGHT_GRID_TRANSPARENCY, interpolation="bilinear")

    key = {}
    key["gas"] = {
        "color": (150, 0, 100),
        "count": 0
    }
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            cell = grid[x,y]
            if isinstance(cell, Cell): #and cell.alive:
                if cell.alive:
                    stats.addCellAlive()
                    try:
                        ax.add_patch(plt.Rectangle((cell.y - 0.5, cell.x - 0.5), 1, 1, color=cell.get_color(top_energy), alpha=cell.get_alpha()))
                    except Exception as e:
                        print(f"Color is {cell.get_color(top_energy)} (current energy {cell.energy} top_energy {top_energy}), Alpha is {cell.get_alpha()} state: {cell.state} alive: {cell.alive} {cell} ({e})")
    """
    for organism in organisms:
        if organism.is_alive():
            color = (random.random(), random.random(), random.random())  # Unique color per organism
            key[organism.organism_id] = {
                "color": color,
                "count": len(organism.cells)
            }
            for cell in organism.cells:
                if cell.alive or cell.state == "inert":
                    if cell.state == "gas":
                        key["gas"]["value"] += 1
                    alpha = 0.3 if cell.state == "gas" else 1
                    cell_color = color if cell.state == "living" else "gray"
                    cell_color = (150, 0, 100) if cell.state == "gas" else cell_color
                    ax.add_patch(plt.Rectangle((cell.y - 0.5, cell.x - 0.5), 1, 1, color=cell_color, alpha=alpha))
            organism.attempt_sentience()  # Check for sentience
            if organism.name:
                print(f"Organism {organism.organism_id} has named itself: {organism.name}")
    """
    full_key=[]
    for k in key:
        v=key[k]
        correct_color=(v["color"][0]/255,v["color"][1]/255,v["color"][2]/255)
        patch = mpatches.Patch(color=correct_color, label=f"{v['count']}")
        full_key.append(patch)
    ax.legend(handles=full_key)

    ax.set_title(f"Step {step + 1} ({stats.cellAliveCount})")
    print(f"Done plotting, {stats.cellAliveCount} cells are alive and displayed. Starting env changes")
    plt.pause(0.1)

    enrich_environment(lightGrid, waifuGrid, inertGrid)  # Replenish nutrients dynamically

    #if step % 100 == 0:  # Stir the environment every 100 steps
    #    stir_environment(grid)
    
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            cell = grid[x,y]
            if isinstance(cell, Cell):
                if cell.step_count < step:
                    cell.step_count = step
                    cell.move(grid, lightGrid, inertGrid)
                    cell.absorb_nutrients(lightGrid)
                    cell.phase_transition()
                    cell.reproduce(grid, lightGrid)
                    cell.decay(lightGrid, inertGrid)
                    cell.waifuSignal(waifuGrid)
                    if cell.energy > top_energy:
                        top_energy = cell.energy
    print("Done with env")
    
    stats.endTurn()

print(stats)

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
