# CELL CLASS FILE: GAME OF WHY
# CHARIS CAT 2024

from matplotlib.colors import hsv_to_rgb
import random
from config import *

cellElderCount = 0
cellYouthCount = 0
cellAdultCount = 0

class Cell:
    topEnergy = 1
    def __init__(self, x, y, stats, environment, organismCheck=None):
        self.id = stats.getCellNextID() # Cell ID
        self.alive = True
        self.environment = environment
        self.role = "general"  # Role of the cell: general, structural, sensory, reproductive
        self.age = 0  # cell age (in turns)
        self.organism = organismCheck  # Tracks which organism this cell belongs to
        self.stats = stats
        self.attrctiveness = CELL_BASE_ATTRACTIVENESS_MIN
        self.turnCount = 0 # turn checker
        self.x = x # position x
        self.y = y # position y

        self.energy = random.uniform(CELL_BASE_ENERGY_MIN, CELL_BASE_ENERGY_MAX)  # Starting energy level
        self.phaseTransition() # Call to set cell state & color

        # INDIVIDUAL CELL BEHAVIOURS
        if self.state == "plasma":
            self.growthRate = random.uniform(CELL_PLASMA_GROWTH_RATE_MIN, CELL_PLASMA_GROWTH_RATE_MAX)  # Energy Absorption
            self.resilience = random.uniform(CELL_PLASMA_RESILIENCE_MIN, CELL_PLASMA_RESILIENCE_MAX)  # 'toughness'
            self.perceptionStrength = random.uniform(CELL_PLASMA_PERCEPTION_MIN, CELL_PLASMA_PERCEPTION_MIN)  # Sensory acuity
            self.speed = random.uniform(CELL_PLASMA_SPEED_MIN, CELL_PLASMA_SPEED_MAX)  # movement speed
            self.lightEmission = random.uniform(CELL_PLASMA_LIGHT_EMISSION_MIN, CELL_PLASMA_LIGHT_EMISSION_MIN)  # Amount of light emitted (e.g., by plasma or bioluminescence)
            self.lightAbsorption = random.uniform(CELL_PLASMA_LIGHT_ABSORPTION_MIN, CELL_PLASMA_LIGHT_ABSORPTION_MAX)  # Ability to absorb light as energy
            self.mutationRate = random.uniform(CELL_PLASMA_MUTATION_RATE_MIN, CELL_PLASMA_MUTATION_RATE_MAX)  # Probability of mutation during reproduction
            self.lifeExpectancy = self.resilience * random.uniform(CELL_PLASMA_DEATH_AGE_MIN, CELL_PLASMA_DEATH_AGE_MAX)
            self.fertilityRate = random.uniform(CELL_PLASMA_FERTILITY_RATE_MIN, CELL_PLASMA_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_PLASMA_FERTILITY_START_AGE_MIN, CELL_PLASMA_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_PLASMA_FERTILITY_END_AGE_MIN, CELL_PLASMA_FERTILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_PLASMA_FERTILITY_ENERGY_MIN, CELL_PLASMA_FERTILITY_ENERGY_MAX)
        elif self.state == "gas":
            self.growthRate = random.uniform(CELL_GAS_GROWTH_RATE_MIN, CELL_GAS_GROWTH_RATE_MAX)
            self.resilience = random.uniform(CELL_GAS_RESILIENCE_MIN, CELL_GAS_RESILIENCE_MAX)
            self.perceptionStrength = random.uniform(CELL_GAS_PERCEPTION_MIN, CELL_GAS_PERCEPTION_MIN)
            self.speed = random.uniform(CELL_GAS_SPEED_MIN, CELL_GAS_SPEED_MAX)
            self.lightEmission = random.uniform(CELL_GAS_LIGHT_EMISSION_MIN, CELL_GAS_LIGHT_EMISSION_MIN)
            self.lightAbsorption = random.uniform(CELL_GAS_LIGHT_ABSORPTION_MIN, CELL_GAS_LIGHT_ABSORPTION_MAX)
            self.mutationRate = random.uniform(CELL_GAS_MUTATION_RATE_MIN, CELL_GAS_MUTATION_RATE_MAX)
            self.lifeExpectancy = self.resilience * random.uniform(CELL_GAS_DEATH_AGE_MIN, CELL_GAS_DEATH_AGE_MAX)
            self.fertilityRate = random.uniform(CELL_GAS_FERTILITY_RATE_MIN, CELL_GAS_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_GAS_FERTILITY_START_AGE_MIN, CELL_GAS_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_GAS_FERTILITY_END_AGE_MIN, CELL_GAS_FERTILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_GAS_FERTILITY_ENERGY_MIN, CELL_GAS_FERTILITY_ENERGY_MAX)
        elif self.state == "liquid":
            self.growthRate = random.uniform(CELL_LIQUID_GROWTH_RATE_MIN, CELL_LIQUID_GROWTH_RATE_MAX)
            self.resilience = random.uniform(CELL_LIQUID_RESILIENCE_MIN, CELL_LIQUID_RESILIENCE_MAX)
            self.perceptionStrength = random.uniform(CELL_LIQUID_PERCEPTION_MIN, CELL_LIQUID_PERCEPTION_MIN)
            self.speed = random.uniform(CELL_LIQUID_SPEED_MIN, CELL_LIQUID_SPEED_MAX)
            self.lightEmission = random.uniform(CELL_LIQUID_LIGHT_EMISSION_MIN, CELL_LIQUID_LIGHT_EMISSION_MIN)
            self.lightAbsorption = random.uniform(CELL_LIQUID_LIGHT_ABSORPTION_MIN, CELL_LIQUID_LIGHT_ABSORPTION_MAX)
            self.mutationRate = random.uniform(CELL_LIQUID_MUTATION_RATE_MIN, CELL_LIQUID_MUTATION_RATE_MAX)
            self.lifeExpectancy = self.resilience * random.uniform(CELL_LIQUID_DEATH_AGE_MIN, CELL_LIQUID_DEATH_AGE_MAX)
            self.fertilityRate = random.uniform(CELL_LIQUID_FERTILITY_RATE_MIN, CELL_LIQUID_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_LIQUID_FERTILITY_START_AGE_MIN, CELL_LIQUID_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_LIQUID_FERTILITY_END_AGE_MIN, CELL_LIQUID_FERTILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_LIQUID_FERTILITY_ENERGY_MIN, CELL_LIQUID_FERTILITY_ENERGY_MAX)
        elif self.state == "mesophase": # CRYSTALLINE
            self.growthRate = random.uniform(CELL_MESOPHASE_GROWTH_RATE_MIN, CELL_MESOPHASE_GROWTH_RATE_MAX)
            self.resilience = random.uniform(CELL_MESOPHASE_RESILIENCE_MIN, CELL_MESOPHASE_RESILIENCE_MAX)
            self.perceptionStrength = random.uniform(CELL_MESOPHASE_PERCEPTION_MIN, CELL_MESOPHASE_PERCEPTION_MIN)
            self.speed = random.uniform(CELL_MESOPHASE_SPEED_MIN, CELL_MESOPHASE_SPEED_MAX)
            self.lightEmission = random.uniform(CELL_MESOPHASE_LIGHT_EMISSION_MIN, CELL_MESOPHASE_LIGHT_EMISSION_MIN)
            self.lightAbsorption = random.uniform(CELL_MESOPHASE_LIGHT_ABSORPTION_MIN, CELL_MESOPHASE_LIGHT_ABSORPTION_MAX)
            self.mutationRate = random.uniform(CELL_MESOPHASE_MUTATION_RATE_MIN, CELL_MESOPHASE_MUTATION_RATE_MAX)
            self.lifeExpectancy = self.resilience * random.uniform(CELL_MESOPHASE_DEATH_AGE_MIN, CELL_MESOPHASE_DEATH_AGE_MAX)
            self.fertilityRate = random.uniform(CELL_MESOPHASE_FERTILITY_RATE_MIN, CELL_MESOPHASE_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_MESOPHASE_FERTILITY_START_AGE_MIN, CELL_MESOPHASE_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_MESOPHASE_FERTILITY_END_AGE_MIN, CELL_MESOPHASE_FERTILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_MESOPHASE_FERTILITY_ENERGY_MIN, CELL_MESOPHASE_FERTILITY_ENERGY_MAX)
        elif self.state == "solid": # CRYSTALLINE
            self.growthRate = random.uniform(CELL_SOLID_GROWTH_RATE_MIN, CELL_SOLID_GROWTH_RATE_MAX)
            self.resilience = random.uniform(CELL_SOLID_RESILIENCE_MIN, CELL_SOLID_RESILIENCE_MAX)
            self.perceptionStrength = random.uniform(CELL_SOLID_PERCEPTION_MIN, CELL_SOLID_PERCEPTION_MIN)
            self.speed = random.uniform(CELL_SOLID_SPEED_MIN, CELL_SOLID_SPEED_MAX)
            self.lightEmission = random.uniform(CELL_SOLID_LIGHT_EMISSION_MIN, CELL_SOLID_LIGHT_EMISSION_MIN)
            self.lightAbsorption = random.uniform(CELL_SOLID_LIGHT_ABSORPTION_MIN, CELL_SOLID_LIGHT_ABSORPTION_MAX)
            self.mutationRate = random.uniform(CELL_SOLID_MUTATION_RATE_MIN, CELL_SOLID_MUTATION_RATE_MAX)
            self.lifeExpectancy = self.resilience * random.uniform(CELL_SOLID_DEATH_AGE_MIN, CELL_SOLID_DEATH_AGE_MAX)
            self.fertilityRate = random.uniform(CELL_SOLID_FERTILITY_RATE_MIN, CELL_SOLID_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_SOLID_FERTILITY_START_AGE_MIN, CELL_SOLID_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_SOLID_FERTILITY_END_AGE_MIN, CELL_SOLID_FERTILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_SOLID_FERTILITY_ENERGY_MIN, CELL_SOLID_FERTILITY_ENERGY_MAX)
        elif self.state == "inert":
            self.growthRate = random.uniform(CELL_INERT_GROWTH_RATE_MIN, CELL_INERT_GROWTH_RATE_MAX)
            self.resilience = random.uniform(CELL_INERT_RESILIENCE_MIN, CELL_INERT_RESILIENCE_MAX)
            self.perceptionStrength = random.uniform(CELL_INERT_PERCEPTION_MIN, CELL_INERT_PERCEPTION_MIN)
            self.speed = random.uniform(CELL_INERT_SPEED_MIN, CELL_INERT_SPEED_MAX)
            self.lightEmission = random.uniform(CELL_INERT_LIGHT_EMISSION_MIN, CELL_INERT_LIGHT_EMISSION_MIN)
            self.lightAbsorption = random.uniform(CELL_INERT_LIGHT_ABSORPTION_MIN, CELL_INERT_LIGHT_ABSORPTION_MAX)
            self.mutationRate = random.uniform(CELL_INERT_MUTATION_RATE_MIN, CELL_INERT_MUTATION_RATE_MAX)
            self.lifeExpectancy = self.resilience * random.uniform(CELL_INERT_DEATH_AGE_MIN, CELL_INERT_DEATH_AGE_MAX)
            self.fertilityRate = random.uniform(CELL_INERT_FERTILITY_RATE_MIN, CELL_INERT_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_INERT_FERTILITY_START_AGE_MIN, CELL_INERT_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_INERT_FERTILITY_END_AGE_MIN, CELL_INERT_FERTIILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_INERT_FERTILITY_ENERGY_MIN, CELL_INERT_FERTILITY_ENERGY_MAX)
        else:
            self.growthRate = random.uniform(CELL_BASE_GROWTH_RATE_MIN, CELL_BASE_GROWTH_RATE_MAX)
            self.resilience = random.uniform(CELL_BASE_RESILIENCE_MIN, CELL_BASE_RESILIENCE_MAX)
            self.perceptionStrength = random.uniform(CELL_BASE_PERCEPTION_MIN, CELL_BASE_PERCEPTION_MIN)
            self.speed = random.uniform(CELL_BASE_SPEED_MIN, CELL_BASE_SPEED_MAX)
            self.lightEmission = random.uniform(CELL_BASE_LIGHT_EMISSION_MIN, CELL_BASE_LIGHT_EMISSION_MIN)
            self.lightAbsorption = random.uniform(CELL_BASE_LIGHT_ABSORPTION_MIN, CELL_BASE_LIGHT_ABSORPTION_MAX)
            self.mutationRate = random.uniform(CELL_BASE_MUTATION_RATE_MIN, CELL_BASE_MUTATION_RATE_MAX)
            self.lifeExpectancy = self.resilience * random.uniform(CELL_BASE_DEATH_AGE_MIN, CELL_BASE_DEATH_AGE_MAX)
            self.fertilityRate = random.uniform(CELL_BASE_FERTILITY_RATE_MIN, CELL_BASE_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_BASE_FERTILITY_START_AGE_MIN, CELL_BASE_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_BASE_FERTILITY_END_AGE_MIN, CELL_BASE_FERTIILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_BASE_FERTILITY_ENERGY_MIN, CELL_BASE_FERTILITY_ENERGY_MAX)


    def moveOrSquish(self, moving, direction):
        dx, dy = direction
        new_x = (self.x + dx) % self.environment.grid.shape[0]
        new_y = (self.y + dy) % self.environment.grid.shape[1]
        # Found an empty space
        if self.environment.canAddCellAt(new_x, new_y):
            self.environment.moveCellTo(new_x, new_y, self)
            print(f"Escaped a death squish!")
            self.stats.addCellDeathEscape()
            self.stats.addCellMove()
            if not self.alive: # if cell is already inert and needs to move, update inertGrid
                self.environment.addInertAt(self.x, self.y, CELL_DEATH_RELEASE_INERT)
            return True
        else:
            cell = self.environment.getCellAt(new_x, new_y)
            if isinstance(cell, Cell):
                if cell.resilience > self.resilience:
                    # the target cell get squished
                    ratio = random.uniform(CELL_DEATH_RELEASE_SQUISH_MIN, CELL_DEATH_RELEASE_SQUISH_MAX)
                    cell.energy += max(0, self.energy * ratio) # Squish release of energy (norty?!)
                    moving.energy += max(0, self.energy * (1-ratio))
                    self.alive = False
                    self.environment.removeCellFromGrid(self)
                    print(f"Died from cuddles. Energy: {self.energy}, lost {(1 / self.resilience) * self.speed} this turn {self}")
                    self.stats.addCellDeath(CELL_DEATH_REASON_SQUISH)
                    self.environment.addInertAt(self.x, self.y, CELL_DEATH_RELEASE_INERT)
                    return False
                else:
                    # the destination cell moves out the way
                    self.environment.getCellAt(new_x, new_y).moveOrSquish(self, direction)
                    self.environment.moveCellTo(new_x, new_y, self)
                    print(f"The Vengabus is Evolving O.o")
                    self.stats.addCellPush()
                    self.stats.addCellMove()
                    if not self.alive:
                        self.environment.addInertAt(self.x, self.y, CELL_DEATH_RELEASE_INERT)
                    
            else:
                print(f"IDK WHAT'S HERE: {cell}")
        return True
        
    def move(self):
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
            new_x = (self.x + dx) % self.environment.grid.shape[0]
            new_y = (self.y + dy) % self.environment.grid.shape[1]
            if self.environment.grid[new_x, new_y] == 0 or \
               self.environment.grid[new_x, new_y] is None or \
               self.environment.grid[new_x, new_y] == "gas":  # Allow passage through gas
                # print(f"Space is empty signal is {abs(lightGrid[new_x, new_y])} * {self.perception_strength}, max_signal is currently {max_signal}")
                # TODO: change that to having "moving towards the highest energy cell it can sense"
                signal = (abs(self.environment.lightGrid[new_x, new_y]) * (self.environment.waifuGrid[new_x, new_y]) * self.perceptionStrength) * ENVIRONMENT_VISIBILITY_MULTIPLIER
                # print(f"env: {lightGrid[new_x, new_y]} wai: {waifuGrid[new_x, new_y]} per: {self.perception_strength}")
                if signal > max_signal:
                    # print(f"Best signal")
                    best_move = (dx, dy)
                    max_signal = signal
            elif self.resilience > self.environment.grid[new_x,new_y].resilience:
                # Current cell resilience sup to target resilience
                # Try to push the target away
                # print(f"Squish time")
                self.environment.grid[new_x,new_y].moveOrSquish(self, (dx, dy))
                best_move = (dx, dy)
                break
            # else:
            #    print(f"Space is full")

        dx, dy = best_move
        new_x = (self.x + dx) % self.environment.grid.shape[0]
        new_y = (self.y + dy) % self.environment.grid.shape[1]
        blockCounter = 0
        if self.environment.grid[new_x, new_y] == 0 or \
            self.environment.grid[new_x, new_y] is None or \
            self.environment.grid[new_x, new_y] == "gas" and blockCounter == 0:  # Move if space is empty or gas
            # print(f"Moving {self.id} from ({self.x}, {self.y}) to ({new_x}, {new_y})")
            self.environment.moveCellTo(new_x, new_y, self)
            self.stats.addCellMove()
        else:
            if (dx, dy) == (0, 1) and blockCounter < 4:
                dx, dy = (1, 0)
                # print(f"Blocked, attempting to move to {new_x, new_y}")
                blockCounter += 1
                self.environment.moveCellTo((self.x + dx) % self.environment.grid.shape[0], (self.y + dy) % self.environment.grid.shape[1], self)
                self.stats.addCellMove()
            if (dx, dy) == (1, 0) and blockCounter < 4:
                dx, dy = (0, -1)
                # print(f"Blocked, attempting to move to {new_x, new_y}")
                blockCounter += 1
                self.environment.moveCellTo((self.x + dx) % self.environment.grid.shape[0], (self.y + dy) % self.environment.grid.shape[1], self)
                self.stats.addCellMove()
            if (dx, dy) == (0, -1) and blockCounter < 4:
                dx, dy = (-1, 0)
                # print(f"Blocked, attempting to move to {new_x, new_y}")
                blockCounter += 1
                self.environment.moveCellTo((self.x + dx) % self.environment.grid.shape[0], (self.y + dy) % self.environment.grid.shape[1], self)
                self.stats.addCellMove()
            if (dx, dy) == (-1, 0) and blockCounter < 4:
                dx, dy = (0, 1)
                # print(f"Blocked, attempting to move to {new_x, new_y}")
                blockCounter += 1
                self.environment.moveCellTo((self.x + dx) % self.environment.grid.shape[0], (self.y + dy) % self.environment.grid.shape[1], self)
                self.stats.addCellMove()
            else:
                if self.x != new_x or self.y != new_y:
                    print(f"Failed moving {self.id} from ({self.x}, {self.y}) to ({new_x}, {new_y})")
                else:
                    print(f"Failed moving {self.id} onto itself")
        
    def getCellColor(self):
        if self.organism:
            if self.organism.name: # sentient = random color picked once
                if not hasattr(self.organism, "color"):
                    self.organism.color = hsv_to_rgb((random.uniform(0, 1), min(1, max(0.8, self.energy / self.topEnergy)), min(max(0.5, self.energy / top_energy), 1)))
                    return self.organism.color
            else: # dark blue
                return hsv_to_rgb((0.6, min(1, max(0.8, self.energy / self.topEnergy)), min(1, max(0.8, self.energy / self.topEnergy))))
        if not self.alive:
            return hsv_to_rgb((self.hue, 1, 0.2))
        else:
            return hsv_to_rgb((self.hue, min(1, max(0.5, self.energy / (self.topEnergy))), min(1, max(0.8, self.energy / self.topEnergy))))

    def absorbNutrients(self):
        if self.alive:
            nutrients = self.environment.getLightAt(self.x, self.y) #lightGrid[self.x, self.y]
            self.energy += nutrients * self.growthRate * 5
            self.environment.depleteLightAt(self.x, self.y, 0.02)
            # self.environment.lightGrid[self.x, self.y] = max(self.environment.lightGrid[self.x, self.y] - 0.02, 0)  # Deplete nutrients

    def emitLight(self):
        if self.state == "plasma": # Plasma cells consistently emit high light
            self.lightEmission = 5
            # lightGrid[self.x, self.y] = min(lightGrid[self.x, self.y] + self.light_emission, 100)
        elif random.random() < 0.01 and self.energy > 120: # Non-plasma cells have a random chance to emit light
            self.lightEmission = 1
            # lightGrid[self.x, self.y] = min(lightGrid[self.x, self.y] + self.light_emission, 100)
        else:
            self.lightEmission = 0
        self.environment.addLightAt(self.x, self.y, self.lightEmission)
            
    def waifuSignal(self):
        if self.alive:
            self.environment.addAttractivenessAt(self.x, self.y, self.attractiveness)
            # waifuGrid[self.x, self.y] = min(waifuGrid[self.x, self.y] + self.attractiveness, 100)
            vibes = self.environment.getAttractivenessAt(self.x, self.y) # waifuGrid[self.x, self.y]
            self.attractiveness += vibes * self.growthRate * 0.5
        else:
            self.environment.setAttractivenessAt(self.x, self.y, 0)
            # waifuGrid[self.x, self.y] = 0

    def senseEnvironment(self):
        if not self.alive:
            return None
        # Detect neighboring states and light levels
        neighbor_states = {}
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = (self.x + dx) % self.environment.grid.shape[0], (self.y + dy) % self.environment.grid.shape[1]
            neighbor_states[(dx, dy)] = {
                "state": self.environment.grid[nx, ny],
                "light": self.environment.grid[nx, ny].lightEmission if isinstance(self.environment.grid[nx, ny], Cell) else 0,
                "rating": self.environment.grid[nx, ny].waifuSignal if isinstance(self.environment.grid[nx, ny], Cell) else 0
            }
        return neighbor_states
        # print(neighbor_states)
            
    # State of the cell: solid, liquid, gas, plasma, inert
    def phaseTransition(self):
        if self.energy > CELL_STATE_PLASMA_ENERGY:
            self.state = "plasma"
            self.hue = random.uniform(CELL_STATE_PLASMA_COLOR_MIN, CELL_STATE_PLASMA_COLOR_MAX)
            self.alpha = random.uniform(CELL_STATE_PLASMA_ALPHA_MIN, CELL_STATE_PLASMA_ALPHA_MAX)
        elif CELL_STATE_GAS_ENERGY < self.energy <= CELL_STATE_PLASMA_ENERGY:
            self.state = "gas"
            self.hue = random.uniform(CELL_STATE_GAS_COLOR_MIN, CELL_STATE_GAS_COLOR_MAX)
            self.alpha = random.uniform(CELL_STATE_GAS_ALPHA_MIN, CELL_STATE_GAS_ALPHA_MAX)
        elif CELL_STATE_LIQUID_ENERGY < self.energy <= CELL_STATE_GAS_ENERGY:
            self.state = "liquid"
            self.hue = random.uniform(CELL_STATE_LIQUID_COLOR_MIN, CELL_STATE_LIQUID_COLOR_MAX)
            self.alpha = random.uniform(CELL_STATE_LIQUID_ALPHA_MIN, CELL_STATE_LIQUID_ALPHA_MAX)
        elif CELL_STATE_MESOPHASE_ENERGY < self.energy <= CELL_STATE_LIQUID_ENERGY:
            self.state = "mesophase"
            self.hue = random.uniform(CELL_STATE_MESOPHASE_COLOR_MIN, CELL_STATE_MESOPHASE_COLOR_MAX)
            self.alpha = random.uniform(CELL_STATE_MESOPHASE_ALPHA_MIN, CELL_STATE_MESOPHASE_ALPHA_MAX)
        elif CELL_STATE_SOLID_ENERGY < self.energy <= CELL_STATE_MESOPHASE_ENERGY:
            self.state = "solid"
            self.hue = random.uniform(CELL_STATE_SOLID_COLOR_MIN, CELL_STATE_SOLID_COLOR_MAX)
            self.alpha = CELL_STATE_SOLID_ALPHA_MIN
        elif CELL_STATE_INERT_ENERGY < self.energy <= CELL_STATE_SOLID_ENERGY:
            self.state = "inert"
            self.hue = self.hue if hasattr(self, "hue") else random.uniform(CELL_STATE_INERT_COLOR_MIN, CELL_STATE_INERT_COLOR_MAX)
            self.alpha = CELL_STATE_INERT_ALPHA_MIN

    def reproduce(self):
        if not self.alive:
            return False
        if not (self.age > self.fertilityAgeMax):
            self.stats.addCellElderly()
            return False
        if not  (self.age < self.fertilityAgeMin):
            self.stats.addCellYouth()
            return False
        self.stats.addCellAdult()
        # reproducing a cell inside an organism (will be done in organism)
        #if self.organism is not None:
        #    return False
        # Generate a baby cell if enough energy
        if random.random() < self.fertilityRate or self.attractiveness > 9 or self.energy > self.fertilityEnergyMin:
            if self.state is "inert": # inert cells 'birth' enrichment onto environment
                inertEnrichValue = (self.age/self.energy)
                self.energy -= enrichInert
                self.environment.addInertAt(self.x, self.y, inertEnrichValue)
                if self.energy <= 0:
                    self.alive = False
                    cellDisintegrationDeathCount += 1
                    cellDisinntegrationCount += 1
                else:
                    cellDisintegrationCount += 1
            else: 
                x, y = (self.x + random.choice([-1, 1])) % self.environment.grid.shape[0], (self.y + random.choice([-1, 1])) % self.environment.grid.shape[1]
                if self.environment.canAddCellAt(x, y):  # Empty spot
                    self.energy = (self.energy/CELL_REPRODUCTION_SUCCESS_COST)
                    baby_cell = Cell(x, y, self.stats, organism=None)
                    baby_cell.growthRate = max(0.5, min(2.0, self.growthRate + random.uniform(CELL_BABY_MUTATION_GROWTH_MIN, CELL_BABY_MUTATION_GROWTH_MAX)))
                    baby_cell.resilience = max(0.5, min(2.0, self.resilience + random.uniform(CELL_BABY_MUTATION_RESILIENCE_MIN, CELL_BABY_MUTATION_RESILIENCE_MAX)))
                    baby_cell.perceptionStrength = max(0.1, min(1.0, self.perceptionStrength + random.uniform(CELL_BABY_MUTATION_PERCEPTION_MIN, CELL_BABY_MUTATION_PERCEPTION_MAX)))
                    baby_cell.speed = max(0.5, min(2.0, self.speed + random.uniform(CELL_BABY_MUTATION_SPEED_MIN, CELL_BABY_MUTATION_SPEED_MAX)))
                    baby_cell.role = random.choice(CELL_ROLES)
                    self.environment.setCellAt(x, y, baby_cell)
                    # print("UNEBEBEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!!!!!!1!!!!!!!!!!!!!1!!!")
                    self.stats.addCellBaby()
                    return True
                else:
                    self.energy = (self.energy/CELL_REPRODUCTION_FAILURE_COST)
                    # print("Tried to UNEBEBEBEBEBEBEBEE BUT NO SPACE LEFT")
                    self.stats.addCellBabyFailed()
                    return False
            return False

    def decay(self):
        if not self.alive:
            return
        self.energy -= (CELL_DECAY_ENERGY_MULTIPLIER / (self.resilience+(self.age)) * self.speed)  # Energy loss increases with speed
        self.age += CELL_DECAY_AGE_PER_TURN
        self.attractiveness = ((self.energy*(CELL_ATTRACTIVENESS_NORM_ENERGY))+(self.age*(CELL_ATTRACTIVENESS_NORM_AGE))+(self.growthRate*CELL_ATTRACTIVENESS_NORM_GROWTH)+(self.resilience*CELL_ATTRACTIVENESS_NORM_RESILIENCE)+(self.perceptionStrength*CELL_ATTRACTIVENESS_NORM_STRENGTH)+(self.speed*CELL_ATTRACTIVENESS_NORM_SPEED)+(self.lightEmission*CELL_ATTRACTIVENESS_NORM_LIGHT_EMISSION))/7
        #print(f"Rated {self.attractiveness}% hot")
        if ((self.energy <= 0) or (self.age > self.lifeExpectancy)):  # Death by starvation or old age
            self.alive = False
            print(f"Died from state {self.state} Energy: {self.energy}, lost {(1 / self.resilience) * self.speed} this turn")
            if self.energy >= 0:
                self.stats.addCellDeath(CELL_DEATH_REASON_AGE)
            else:
                self.stats.addCellDeath(CELL_DEATH_REASON_STARVATION)
            self.energy = 0
            self.state = "inert"
            self.environment.addLightAt(self.x, self.y, CELL_DEATH_RELEASE_LIGHT)
            self.environment.addInertAt(self.x, self.y, CELL_DEATH_RELEASE_INERT)
            #lightGrid[self.x, self.y] += CELL_DEATH_RELEASE_LIGHT  # Dead cells release light for some reason
            #inertGrid[self.x, self.y] += CELL_DEATH_RELEASE_INERT # Drop inert resources onto inert grid

    def needTurn(self, turn):
        return self.turnCount < turn

    def runLoop(self, turn):
        self.turnCount = turn
        self.move()
        self.absorbNutrients()
        self.phaseTransition()
        self.reproduce()
        self.decay()
        self.waifuSignal()
        if self.energy > self.topEnergy:
            self.topEnergy = self.energy
