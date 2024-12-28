import numpy as np
import matplotlib.pyplot as plt
import random
import matplotlib.patches as mpatches
from matplotlib.colors import hsv_to_rgb
from functools import partial
from scipy.ndimage import gaussian_filter
from matplotlib.colors import LinearSegmentedColormap

from config import GRID_SIZE, NUM_STEPS, INITIAL_CELL_COUNT, CELL_ROLES, PLASMA_ENERGY, GAS_ENERGY, LIQUID_ENERGY, SOLID_ENERGY, INERT_ENERGY, CELL_FERTILITY_MIN_AGE, CELL_FERTILITY_MAX_AGE, CELL_FERTILITY_CHANCE, CELL_FERTILITY_ENERGY, CELL_REPRODUCTION_FAILURE_COST, CELL_REPRODUCTION_SUCCESS_COST, CELL_BASE_MUTATION_RATE, CELL_BASE_MIN_GROWTH_RATE, CELL_BASE_MAX_GROWTH_RATE, CELL_BASE_MIN_RESILIENCE, CELL_BASE_MAX_RESILIENCE, CELL_BASE_MIN_PERCEPTION, CELL_BASE_MAX_PERCEPTION, CELL_BASE_MIN_SPEED, CELL_BASE_MAX_SPEED, CELL_BASE_LIGHT_EMISSION

# TURN STATISTICS
counter = 0
babyCounter = 0
babysThisTurn = babyCounter
deathSquishCounter = 0
deathsThisTurn = deathSquishCounter

class Cell:
    def __init__(self, x, y, id, organism=None):
        self.id = id
        self.step_count = 0
        self.x = x
        self.y = y
        self.energy = random.uniform(0, 200)  # Starting energy level
        self.age = 0  # Age of the cell
        self.mutation_rate = CELL_BASE_MUTATION_RATE  # Probability of mutation during reproduction
        self.alive = True
        self.role = "general"  # Role of the cell: general, structural, sensory, reproductive
        self.growth_rate = random.uniform(CELL_BASE_MIN_GROWTH_RATE, CELL_BASE_MAX_GROWTH_RATE)  # Genetic trait for energy absorption
        self.resilience = random.uniform(CELL_BASE_MIN_RESILIENCE, CELL_BASE_MAX_RESILIENCE)  # Resistance to harsh environments
        self.perception_strength = random.uniform(CELL_BASE_MIN_PERCEPTION, CELL_BASE_MAX_PERCEPTION)  # Communication ability
        self.speed = random.uniform(CELL_BASE_MIN_SPEED, CELL_BASE_MAX_SPEED)  # Speed of movement
        self.phase_transition() # Call to set cell state & color
        self.light_emission = CELL_BASE_LIGHT_EMISSION  # Amount of light emitted (e.g., by plasma or bioluminescence)
        self.light_absorption = random.uniform(0.1, 1.0)  # Ability to absorb light
        self.genome = {
            'growth_rate': self.growth_rate,
            'resilience': self.resilience,
            'perception_strength': self.perception_strength,
            'speed': self.speed,
            'role': self.role
        }
        self.organism = organism  # Tracks which organism this cell belongs to
        self.waifuRating = 0

    def move_or_squish(self, moving, direction, grid, inertGrid, deathCounter):
        dx, dy = direction
        new_x = (self.x + dx) % grid.shape[0]
        new_y = (self.y + dy) % grid.shape[1]
        # Reached the end of the grid
        if new_x >= grid.shape[0] or new_y >= grid.shape[1]:
            grid[self.x, self.y] = None
            moving.energy += max(0, (random.uniform(0.9, 1) * self.energy))
            self.alive = False
            print(f"Died from wall cuddles. Energy: {self.energy}, lost {(1 / self.resilience) * self.speed} this turn")
            deathCounter += 1
            inertGrid[self.x, self.y] += 300
            return False
        # Found an empty space
        if grid[new_x, new_y] == 0 or grid[new_x, new_y] is None:
            grid[self.x, self.y] = None
            self.x = new_x
            self.y = new_y
            grid[self.x, self.y] = self
            print(f"Escaped a death squish!")
            if not self.alive:
                inertGrid[self.x, self.y] += 300
            return True
        else:
            if isinstance(grid[new_x, new_y], Cell):
                if grid[new_x, new_y].resilience > grid[self.x,self.y].resilience:
                    # the target cell get squished
                    ratio = random.uniform(0.4, 0.6)
                    grid[new_x, new_y].energy += max(0, self.energy * ratio)
                    moving.energy += max(0, self.energy * (1-ratio))
                    self.alive = False
                    grid[self.x, self.y] = None
                    print(f"Died from cuddles. Energy: {self.energy}, lost {(1 / self.resilience) * self.speed} this turn {self}")
                    deathCounter += 1
                    inertGrid[self.x, self.y] += 300
                    return False
                else:
                    # the destination cell moves out the way
                    grid[new_x, new_y].move_or_squish(self, direction, grid, inertGrid)
                    grid[self.x, self.y] = None
                    self.x, self.y = (new_x, new_y)
                    grid[self.x, self.y] = self
                    print(f"Narrowly escaped a death squish!")
                    if not self.alive:
                        inertGrid[self.x, self.y] += 300
                    
            else:
                print(f"IDK WHAT'S HERE: {grid[new_x, new_y]}")
        return True
        
    def move(self, grid, environment, inertGrid):
        if not self.alive or self.energy < 1:
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
                # print(f"Space is empty signal is {abs(environment[new_x, new_y])} * {self.perception_strength}, max_signal is currently {max_signal}")
                # TODO: change that to having "moving towards the highest energy cell it can sense"
                signal = abs(environment[new_x, new_y]) * (waifuGrid[new_x, new_y]) * self.perception_strength
                # print(f"env: {environment[new_x, new_y]} wai: {waifuGrid[new_x, new_y]} per: {self.perception_strength}")
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
        else:
            if (dx, dy) == (0, 1):
                dx, dy = (1, 0)
                # print(f"Blocked, attempting to move to {new_x, new_y}")
                blockCounter += 1
                grid[self.x, self.y] = None
                self.x, self.y = (self.x + dx) % grid.shape[0], (self.y + dy) % grid.shape[1]
                grid[self.x, self.y] = self
            if (dx, dy) == (1, 0):
                dx, dy = (0, -1)
                # print(f"Blocked, attempting to move to {new_x, new_y}")
                blockCounter += 1
                grid[self.x, self.y] = None
                self.x, self.y = (self.x + dx) % grid.shape[0], (self.y + dy) % grid.shape[1]
                grid[self.x, self.y] = self
            if (dx, dy) == (0, -1):
                dx, dy = (-1, 0)
                # print(f"Blocked, attempting to move to {new_x, new_y}")
                blockCounter += 1
                grid[self.x, self.y] = None
                self.x, self.y = (self.x + dx) % grid.shape[0], (self.y + dy) % grid.shape[1]
                grid[self.x, self.y] = self
            if (dx, dy) == (-1, 0):
                dx, dy = (0, 1)
                # print(f"Blocked, attempting to move to {new_x, new_y}")
                blockCounter += 1
                grid[self.x, self.y] = None
                self.x, self.y = (self.x + dx) % grid.shape[0], (self.y + dy) % grid.shape[1]
                grid[self.x, self.y] = self
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

    def absorb_nutrients(self, environment):
        if self.alive:
            nutrients = environment[self.x, self.y]
            self.energy += nutrients * self.growth_rate * 5
            environment[self.x, self.y] = max(environment[self.x, self.y] - 0.02, 0)  # Deplete nutrients

    def emit_light(self, environment):
        if self.state == "plasma": # Plasma cells consistently emit high light
            self.light_emission = 5
            environment[self.x, self.y] = min(environment[self.x, self.y] + self.light_emission, 100)
        elif random.random() < 0.01 and self.energy > 120: # Non-plasma cells have a random chance to emit light
            self.light_emission = 1
            environment[self.x, self.y] = min(environment[self.x, self.y] + self.light_emission, 100)
        else:
            self.light_emission = 0
            
    def waifuSignal(self, waifuGrid):
        if self.alive:
            waifuGrid[self.x, self.y] = min(waifuGrid[self.x, self.y] + self.waifuRating, 100)
            vibes = waifuGrid[self.x, self.y]
            self.waifuRating += vibes * self.growth_rate * 0.5
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
        if self.energy > PLASMA_ENERGY:
            self.state = "plasma"
            self.hue = random.uniform(0.0, 0.1)
        elif GAS_ENERGY < self.energy <= PLASMA_ENERGY:
            self.state = "gas"
            self.hue = random.uniform(0.7, 0.75)
        elif LIQUID_ENERGY < self.energy <= GAS_ENERGY:
            self.state = "liquid"
            self.hue = random.uniform(0.5, 0.7)
        elif SOLID_ENERGY < self.energy <= LIQUID_ENERGY:
            self.state = "solid"
            self.hue = random.uniform(0.15, 0.35)
        elif INERT_ENERGY < self.energy <= SOLID_ENERGY:
            self.state = "inert"
            self.hue = self.hue if hasattr(self, "hue") else 0

    def reproduce(self, grid, environment, counter):
        if not self.alive or (self.age > CELL_FERTILITY_MAX_AGE) or (self.age < CELL_FERTILITY_MIN_AGE):
            return
        # reproducing a cell inside an organism (will be done in organism)
        #if self.organism is not None:
        #    return
        # Generate a baby cell if enough energy
        if random.random() < CELL_FERTILITY_CHANCE or self.waifuRating > 9 or self.energy > CELL_FERTILITY_ENERGY:
            x, y = (cell.x + random.choice([-1, 1])) % grid.shape[0], (cell.y + random.choice([-1, 1])) % grid.shape[1]
            if grid[x, y] == 0 or grid[x, y] is None:  # Empty spot
                babyCounter += 1
                counter += 1
                self.energy = (self.energy/CELL_REPRODUCTION_SUCCESS_COST)
                baby_cell = Cell(x, y, counter, organism=None)
                baby_cell.growth_rate = max(0.5, min(2.0, cell.growth_rate + random.uniform(-0.1, 0.1)))
                baby_cell.resilience = max(0.5, min(2.0, cell.resilience + random.uniform(-0.1, 0.1)))
                baby_cell.perception_strength = max(0.1, min(1.0, cell.perception_strength + random.uniform(-0.05, 0.05)))
                baby_cell.speed = max(0.5, min(2.0, cell.speed + random.uniform(-0.1, 0.1)))
                baby_cell.role = random.choice(CELL_ROLES)
                grid[x, y] = baby_cell
                # print("UNEBEBEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!!!!!!1!!!!!!!!!!!!!1!!!")
                return babyCounter, counter
            else:
                self.energy = (self.energy/CELL_REPRODUCTION_FAILURE_COST)
                # print("Tried to UNEBEBEBEBEBEBEBEE BUT NO SPACE LEFT")
                return babyCounter, counter

    def decay(self, environment, inertGrid):
        if not self.alive:
            return
        self.energy -= (1 / (self.resilience+(self.age/100)) * self.speed)  # Energy loss increases with speed
        self.age += 1
        self.waifuRating = ((self.energy)+(self.age)+(self.growth_rate*100)+(self.resilience*100)+(self.perception_strength*100)+(self.speed*100)+(self.light_emission*100))/70
        #print(f"Rated {self.waifuRating}% hot")
        if self.energy <= 0 or self.age > (self.resilience * random.uniform(80, 500)):  # Death by starvation or old age
            self.alive = False
            print(f"Died from state {self.state} Energy: {self.energy}, lost {(1 / self.resilience) * self.speed} this turn")
            self.energy = 0
            self.state = "inert"
            environment[self.x, self.y] += 0.5  # Dead cells enrich the environment
            inertGrid[self.x, self.y] += 200

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
environment = np.random.random((GRID_SIZE, GRID_SIZE)) * 5  # Light levels
waifuGrid = np.zeros((GRID_SIZE, GRID_SIZE))
inertGrid = np.zeros((GRID_SIZE, GRID_SIZE)) # Fully decayed inerts

# Enrich environment dynamically
def enrich_environment(environment, waifuGrid, inertGrid):
    # Brighten some random areas
    for _ in range(5):  # Number of light sources
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        environment[x, y] = min(environment[x, y] + 0.1, 5)  # Cap at max brightness
    environment -= 0.05
    environment = np.clip(environment, 0, 100)
    waifuGrid -= 0.05
    inertGrid -= 0.01
    #print(environment)
    #print(np.min(environment))
    #print(np.max(environment))
    #environment = gaussian_filter(environment, sigma=1)  # sigma = more/less blur
    #print(environment)


def stir_environment(grid):
    # Randomly displace cells to "stir things up"
    for _ in range(100):  # Number of cells to displace
        x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
        if isinstance(grid[x, y], Cell):
            dx, dy = random.choice([(0, 1), (1, 0), (0, -1), (-1, 0)])
            new_x = (x + dx) % GRID_SIZE
            new_y = (y + dy) % GRID_SIZE
            if grid[new_x, new_y] == 0:
                grid[new_x, new_y] = grid[x, y]
                grid[x, y] = 0

def on_click(counter, event):
    # Handles mouse clicks to place cells
    if event.xdata is None or event.ydata is None:
        return
    x, y = int(event.ydata), int(event.xdata)
    if grid[x, y] == 0 or grid[x, y] is None:
        new_cell = Cell(x, y, counter, organism=None)
        counter += 1
        new_cell.role = random.choice(CELL_ROLES)
        grid[x, y] = new_cell
        print(f"Placed a {new_cell.role} cell at ({x}, {y})")

cells = []
for _ in range(INITIAL_CELL_COUNT):
    x, y = random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)
    organism = Organism(next_organism_id)
    next_organism_id += 1
    new_cell = Cell(x, y, counter, organism=organism)
    counter += 1
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
cid = fig.canvas.mpl_connect('button_press_event', partial(on_click, counter))
top_energy = 100
for step in range(NUM_STEPS):
    print(f"Step {step} start")
    ax.clear()
    #ax.imshow(gridSize, alpha=0.5)
    ax.imshow(inertGrid, cmap=terrain_colormap, alpha=0.8)
    ax.imshow(waifuGrid, cmap="BuPu", alpha=0.6, interpolation="bilinear")
    ax.imshow(environment, cmap=purple_yellow_colormap, alpha=0.6, interpolation="bilinear")

    key = {}
    key["gas"] = {
        "color": (150, 0, 100),
        "count": 0
    }
    alive = 0
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            cell = grid[x,y]
            if isinstance(cell, Cell): #and cell.alive:
                if cell.alive:
                    alive += 1
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

    ax.set_title(f"Step {step + 1} ({alive})")
    print(f"Done plotting, {alive} cells are alive and displayed. Starting env changes")
    plt.pause(0.1)
    plt.show(block=True)  # Keeps the figure window open until you close it manually

    enrich_environment(environment, waifuGrid, inertGrid)  # Replenish nutrients dynamically

    #if step % 100 == 0:  # Stir the environment every 100 steps
    #    stir_environment(grid)
    
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            cell = grid[x,y]
            if isinstance(cell, Cell):
                if cell.step_count < step:
                    cell.step_count = step
                    cell.move(grid, environment, inertGrid)
                    cell.absorb_nutrients(environment)
                    cell.phase_transition()
                    cell.reproduce(grid, environment, counter)
                    cell.decay(environment, inertGrid)
                    cell.waifuSignal(waifuGrid)
                    if cell.energy > top_energy:
                        top_energy = cell.energy
    print("Done with env")
    
print(f"Turn Summary: There were {babysThisTurn} babies born, {deathsThisTurn} cells died, ")
    """
    new_organisms = []
    for organism in organisms:
        for cell in organism.cells:
            cell.move(grid, environment)
            cell.absorb_nutrients(environment)
            cell.phase_transition(environment)
            baby = cell.reproduce(organism, grid, environment)
            if baby:
                new_organisms.append(baby)
            cell.decay(environment)

    organisms.extend(new_organisms)
    organisms = [org for org in organisms if org.is_alive()]
    """
