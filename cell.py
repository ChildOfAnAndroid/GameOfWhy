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
    CellAttractivenessTopRecord = CELL_ATTRACTIVENESS_TOP_RECORD_INIT
    ratioResult = 0
    attractivenessGain = 0
    def __init__(self, x, y, stats, environment, organismCheck=None):
        self.id = stats.getCellNextID() # Cell ID
        self.alive = True
        self.environment = environment
        self.role = "general"  # Role of the cell: general, structural, sensory, reproductive
        self.age = 0  # cell age (in turns)
        self.organism = organismCheck  # Tracks which organism this cell belongs to
        self.stats = stats
        self.attractiveness = CELL_BASE_ATTRACTIVENESS_MIN
        self.growthDecayRate = CELL_BASE_GROWTH_DECAY_RATE
        self.turnCount = 0 # turn checker
        self.x = x # position x
        self.y = y # position y
        self.memory = []
        self.previousAlive = 0
        self.topEnergyDecay = 0

        self.energy = random.uniform(CELL_BASE_ENERGY_MIN, CELL_BASE_ENERGY_MAX)  # Starting energy level
        self.phaseTransition() # Call to set cell state & color

        # INDIVIDUAL CELL BEHAVIOURS
        if self.state == "plasma":
            self.growthRate = random.uniform(CELL_PLASMA_GROWTH_RATE_MIN, CELL_PLASMA_GROWTH_RATE_MAX)  # Energy Absorption
            self.resilience = random.uniform(CELL_PLASMA_RESILIENCE_MIN, CELL_PLASMA_RESILIENCE_MAX)  # 'toughness'
            self.perceptionStrength = random.uniform(CELL_PLASMA_PERCEPTION_MIN, CELL_PLASMA_PERCEPTION_MAX)  # Sensory acuity
            self.speed = random.uniform(CELL_PLASMA_SPEED_MIN, CELL_PLASMA_SPEED_MAX)  # movement speed
            self.lightEmission = random.uniform(CELL_PLASMA_LIGHT_EMISSION_MIN, CELL_PLASMA_LIGHT_EMISSION_MAX)  # Amount of light emitted (e.g., by plasma or bioluminescence)
            self.lightAbsorption = random.uniform(CELL_PLASMA_LIGHT_ABSORPTION_MIN, CELL_PLASMA_LIGHT_ABSORPTION_MAX)  # Ability to absorb light as energy
            self.mutationRate = random.uniform(CELL_PLASMA_MUTATION_RATE_MIN, CELL_PLASMA_MUTATION_RATE_MAX)  # Probability of mutation during reproduction
            self.lifeExpectancyMin = random.uniform(0.95, 1.05) * CELL_PLASMA_DEATH_AGE_MAX
            self.lifeExpectancyMax = random.uniform(0.95, 1.05) * CELL_PLASMA_DEATH_AGE_MAX
            self.lifeExpectancy = random.uniform(self.lifeExpectancyMin, self.lifeExpectancyMax)
            self.fertilityRate = random.uniform(CELL_PLASMA_FERTILITY_RATE_MIN, CELL_PLASMA_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_PLASMA_FERTILITY_START_AGE_MIN, CELL_PLASMA_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_PLASMA_FERTILITY_END_AGE_MIN, CELL_PLASMA_FERTILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_PLASMA_FERTILITY_ENERGY_MIN, CELL_PLASMA_FERTILITY_ENERGY_MAX)
            self.mass = random.uniform(CELL_PLASMA_MASS_MIN, CELL_PLASMA_MASS_MAX)
        elif self.state == "gas":
            self.growthRate = random.uniform(CELL_GAS_GROWTH_RATE_MIN, CELL_GAS_GROWTH_RATE_MAX)
            self.resilience = random.uniform(CELL_GAS_RESILIENCE_MIN, CELL_GAS_RESILIENCE_MAX)
            self.perceptionStrength = random.uniform(CELL_GAS_PERCEPTION_MIN, CELL_GAS_PERCEPTION_MAX)
            self.speed = random.uniform(CELL_GAS_SPEED_MIN, CELL_GAS_SPEED_MAX)
            self.lightEmission = random.uniform(CELL_GAS_LIGHT_EMISSION_MIN, CELL_GAS_LIGHT_EMISSION_MAX)
            self.lightAbsorption = random.uniform(CELL_GAS_LIGHT_ABSORPTION_MIN, CELL_GAS_LIGHT_ABSORPTION_MAX)
            self.mutationRate = random.uniform(CELL_GAS_MUTATION_RATE_MIN, CELL_GAS_MUTATION_RATE_MAX)
            self.lifeExpectancyMin = random.uniform(0.95, 1.05) * CELL_GAS_DEATH_AGE_MAX
            self.lifeExpectancyMax = random.uniform(0.95, 1.05) * CELL_GAS_DEATH_AGE_MAX
            self.lifeExpectancy = random.uniform(self.lifeExpectancyMin, self.lifeExpectancyMax)
            self.fertilityRate = random.uniform(CELL_GAS_FERTILITY_RATE_MIN, CELL_GAS_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_GAS_FERTILITY_START_AGE_MIN, CELL_GAS_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_GAS_FERTILITY_END_AGE_MIN, CELL_GAS_FERTILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_GAS_FERTILITY_ENERGY_MIN, CELL_GAS_FERTILITY_ENERGY_MAX)
            self.mass = random.uniform(CELL_GAS_MASS_MIN, CELL_GAS_MASS_MAX)
        elif self.state == "liquid":
            self.growthRate = random.uniform(CELL_LIQUID_GROWTH_RATE_MIN, CELL_LIQUID_GROWTH_RATE_MAX)
            self.resilience = random.uniform(CELL_LIQUID_RESILIENCE_MIN, CELL_LIQUID_RESILIENCE_MAX)
            self.perceptionStrength = random.uniform(CELL_LIQUID_PERCEPTION_MIN, CELL_LIQUID_PERCEPTION_MAX)
            self.speed = random.uniform(CELL_LIQUID_SPEED_MIN, CELL_LIQUID_SPEED_MAX)
            self.lightEmission = random.uniform(CELL_LIQUID_LIGHT_EMISSION_MIN, CELL_LIQUID_LIGHT_EMISSION_MAX)
            self.lightAbsorption = random.uniform(CELL_LIQUID_LIGHT_ABSORPTION_MIN, CELL_LIQUID_LIGHT_ABSORPTION_MAX)
            self.mutationRate = random.uniform(CELL_LIQUID_MUTATION_RATE_MIN, CELL_LIQUID_MUTATION_RATE_MAX)
            self.lifeExpectancyMin = random.uniform(0.95, 1.05) * CELL_LIQUID_DEATH_AGE_MAX
            self.lifeExpectancyMax = random.uniform(0.95, 1.05) * CELL_LIQUID_DEATH_AGE_MAX
            self.lifeExpectancy = random.uniform(self.lifeExpectancyMin, self.lifeExpectancyMax)
            self.fertilityRate = random.uniform(CELL_LIQUID_FERTILITY_RATE_MIN, CELL_LIQUID_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_LIQUID_FERTILITY_START_AGE_MIN, CELL_LIQUID_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_LIQUID_FERTILITY_END_AGE_MIN, CELL_LIQUID_FERTILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_LIQUID_FERTILITY_ENERGY_MIN, CELL_LIQUID_FERTILITY_ENERGY_MAX)
            self.mass = random.uniform(CELL_LIQUID_MASS_MIN, CELL_LIQUID_MASS_MAX)
        elif self.state == "mesophase":
            self.growthRate = random.uniform(CELL_MESOPHASE_GROWTH_RATE_MIN, CELL_MESOPHASE_GROWTH_RATE_MAX)
            self.resilience = random.uniform(CELL_MESOPHASE_RESILIENCE_MIN, CELL_MESOPHASE_RESILIENCE_MAX)
            self.perceptionStrength = random.uniform(CELL_MESOPHASE_PERCEPTION_MIN, CELL_MESOPHASE_PERCEPTION_MAX)
            self.speed = random.uniform(CELL_MESOPHASE_SPEED_MIN, CELL_MESOPHASE_SPEED_MAX)
            self.lightEmission = random.uniform(CELL_MESOPHASE_LIGHT_EMISSION_MIN, CELL_MESOPHASE_LIGHT_EMISSION_MAX)
            self.lightAbsorption = random.uniform(CELL_MESOPHASE_LIGHT_ABSORPTION_MIN, CELL_MESOPHASE_LIGHT_ABSORPTION_MAX)
            self.mutationRate = random.uniform(CELL_MESOPHASE_MUTATION_RATE_MIN, CELL_MESOPHASE_MUTATION_RATE_MAX)
            self.lifeExpectancyMin = random.uniform(0.95, 1.05) * CELL_MESOPHASE_DEATH_AGE_MAX
            self.lifeExpectancyMax = random.uniform(0.95, 1.05) * CELL_MESOPHASE_DEATH_AGE_MAX
            self.lifeExpectancy = random.uniform(self.lifeExpectancyMin, self.lifeExpectancyMax)
            self.fertilityRate = random.uniform(CELL_MESOPHASE_FERTILITY_RATE_MIN, CELL_MESOPHASE_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_MESOPHASE_FERTILITY_START_AGE_MIN, CELL_MESOPHASE_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_MESOPHASE_FERTILITY_END_AGE_MIN, CELL_MESOPHASE_FERTILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_MESOPHASE_FERTILITY_ENERGY_MIN, CELL_MESOPHASE_FERTILITY_ENERGY_MAX)
            self.mass = random.uniform(CELL_MESOPHASE_MASS_MIN, CELL_MESOPHASE_MASS_MAX)
        elif self.state == "solid": # CRYSTALLINE
            self.growthRate = random.uniform(CELL_SOLID_GROWTH_RATE_MIN, CELL_SOLID_GROWTH_RATE_MAX)
            self.resilience = random.uniform(CELL_SOLID_RESILIENCE_MIN, CELL_SOLID_RESILIENCE_MAX)
            self.perceptionStrength = random.uniform(CELL_SOLID_PERCEPTION_MIN, CELL_SOLID_PERCEPTION_MAX)
            self.speed = random.uniform(CELL_SOLID_SPEED_MIN, CELL_SOLID_SPEED_MAX)
            self.lightEmission = random.uniform(CELL_SOLID_LIGHT_EMISSION_MIN, CELL_SOLID_LIGHT_EMISSION_MAX)
            self.lightAbsorption = random.uniform(CELL_SOLID_LIGHT_ABSORPTION_MIN, CELL_SOLID_LIGHT_ABSORPTION_MAX)
            self.mutationRate = random.uniform(CELL_SOLID_MUTATION_RATE_MIN, CELL_SOLID_MUTATION_RATE_MAX)
            self.lifeExpectancyMin = random.uniform(0.95, 1.05) * CELL_SOLID_DEATH_AGE_MAX
            self.lifeExpectancyMax = random.uniform(0.95, 1.05) * CELL_SOLID_DEATH_AGE_MAX
            self.lifeExpectancy = random.uniform(self.lifeExpectancyMin, self.lifeExpectancyMax)
            self.fertilityRate = random.uniform(CELL_SOLID_FERTILITY_RATE_MIN, CELL_SOLID_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_SOLID_FERTILITY_START_AGE_MIN, CELL_SOLID_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_SOLID_FERTILITY_END_AGE_MIN, CELL_SOLID_FERTILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_SOLID_FERTILITY_ENERGY_MIN, CELL_SOLID_FERTILITY_ENERGY_MAX)
            self.mass = random.uniform(CELL_SOLID_MASS_MIN, CELL_SOLID_MASS_MAX)
        elif self.state == "inert":
            self.growthRate = random.uniform(CELL_INERT_GROWTH_RATE_MIN, CELL_INERT_GROWTH_RATE_MAX)
            self.resilience = random.uniform(CELL_INERT_RESILIENCE_MIN, CELL_INERT_RESILIENCE_MAX)
            self.perceptionStrength = random.uniform(CELL_INERT_PERCEPTION_MIN, CELL_INERT_PERCEPTION_MAX)
            self.speed = random.uniform(CELL_INERT_SPEED_MIN, CELL_INERT_SPEED_MAX)
            self.lightEmission = random.uniform(CELL_INERT_LIGHT_EMISSION_MIN, CELL_INERT_LIGHT_EMISSION_MAX)
            self.lightAbsorption = random.uniform(CELL_INERT_LIGHT_ABSORPTION_MIN, CELL_INERT_LIGHT_ABSORPTION_MAX)
            self.mutationRate = random.uniform(CELL_INERT_MUTATION_RATE_MIN, CELL_INERT_MUTATION_RATE_MAX)
            self.lifeExpectancyMin = random.uniform(0.95, 1.05) * CELL_INERT_DEATH_AGE_MAX
            self.lifeExpectancyMax = random.uniform(0.95, 1.05) * CELL_INERT_DEATH_AGE_MAX
            self.lifeExpectancy = random.uniform(self.lifeExpectancyMin, self.lifeExpectancyMax)
            self.fertilityRate = random.uniform(CELL_INERT_FERTILITY_RATE_MIN, CELL_INERT_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_INERT_FERTILITY_START_AGE_MIN, CELL_INERT_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_INERT_FERTILITY_END_AGE_MIN, CELL_INERT_FERTILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_INERT_FERTILITY_ENERGY_MIN, CELL_INERT_FERTILITY_ENERGY_MAX)
            self.mass = random.uniform(CELL_INERT_MASS_MIN, CELL_INERT_MASS_MAX)
        else:
            self.growthRate = random.uniform(CELL_BASE_GROWTH_RATE_MIN, CELL_BASE_GROWTH_RATE_MAX)
            self.resilience = random.uniform(CELL_BASE_RESILIENCE_MIN, CELL_BASE_RESILIENCE_MAX)
            self.perceptionStrength = random.uniform(CELL_BASE_PERCEPTION_MIN, CELL_BASE_PERCEPTION_MAX)
            self.speed = random.uniform(CELL_BASE_SPEED_MIN, CELL_BASE_SPEED_MAX)
            self.lightEmission = random.uniform(CELL_BASE_LIGHT_EMISSION_MIN, CELL_BASE_LIGHT_EMISSION_MAX)
            self.lightAbsorption = random.uniform(CELL_BASE_LIGHT_ABSORPTION_MIN, CELL_BASE_LIGHT_ABSORPTION_MAX)
            self.mutationRate = random.uniform(CELL_BASE_MUTATION_RATE_MIN, CELL_BASE_MUTATION_RATE_MAX)
            self.lifeExpectancyMin = random.uniform(0.95, 1.05) * CELL_BASE_DEATH_AGE_MAX
            self.lifeExpectancyMax = random.uniform(0.95, 1.05) * CELL_BASE_DEATH_AGE_MAX
            self.lifeExpectancy = random.uniform(self.lifeExpectancyMin, self.lifeExpectancyMax)
            self.fertilityRate = random.uniform(CELL_BASE_FERTILITY_RATE_MIN, CELL_BASE_FERTILITY_RATE_MAX)
            self.fertilityAgeMin = random.uniform(CELL_BASE_FERTILITY_START_AGE_MIN, CELL_BASE_FERTILITY_START_AGE_MAX)
            self.fertilityAgeMax = random.uniform(CELL_BASE_FERTILITY_END_AGE_MIN, CELL_BASE_FERTILITY_END_AGE_MAX)
            self.fertilityEnergyMin = random.uniform(CELL_BASE_FERTILITY_ENERGY_MIN, CELL_BASE_FERTILITY_ENERGY_MAX)
            self.mass = random.uniform(CELL_BASE_MASS_MIN, CELL_BASE_MASS_MAX)
    
    def moveOrSquish(self, moving, direction):
        dx, dy = direction
        new_x = (self.x + dx) % self.environment.grid.shape[0]
        new_y = (self.y + dy) % self.environment.grid.shape[1]
        # Use signalGrid for perception-based movement
        signal_at_target = self.environment.signalGrid[new_x, new_y]

        # Found an empty space
        if self.environment.canAddCellAt(new_x, new_y):
            self.environment.moveCellTo(new_x, new_y, self)
            print(f"Escaped a death squish! Ran to signal {signal_at_target}")
            self.stats.addCellDeathEscape()
            self.stats.addCellMove()
            self.resilience += random.uniform(0,0.2)*self.resilience
            self.energy -= random.uniform(0,0.2)*self.energy
            self.memory.append((self.turnCount, "Escaped a death squish!", {signal_at_target}))
            if not self.alive: # if cell is already inert and needs to move, update inertGrid
                self.environment.addInertAt(self.x, self.y, (random.uniform(0.8, 1.2) * CELL_DEATH_RELEASE_INERT))
            return True

        cell = self.environment.getCellAt(new_x, new_y)
        if isinstance(cell, Cell):
            #if cell.speed < (self.speed):
            if cell.resilience > (self.resilience*2):
                # the target cell get squished
                ratio = random.uniform(CELL_DEATH_RELEASE_SQUISH_MIN, CELL_DEATH_RELEASE_SQUISH_MAX)
                squishEnergyTransfer = max(0, self.energy * ratio) # Squish release of energy (norty?!)
                cell.energy += squishEnergyTransfer
                self.alive = False
                self.environment.removeCellFromGrid(self)
                print(f"Died from cuddles. Energy: {self.energy}, lost {squishEnergyTransfer} this turn")
                self.memory.append((self.turnCount, "Died from cuddles", squishEnergyTransfer))
                self.stats.addCellDeath(CELL_DEATH_REASON_SQUISH)
                self.environment.addInertAt(self.x, self.y, (random.uniform(CELL_DEATH_RELEASE_SQUISH_MIN, CELL_DEATH_RELEASE_SQUISH_MIN)))
                return False
            
            else:
                # The destination cell attempts to move away
                cell.moveOrSquish(self, direction)
                if self.environment.canAddCellAt(new_x, new_y):
                    self.environment.moveCellTo(new_x, new_y, self)
                    print(f"The Vengabus is Evolving O.o at signal {signal_at_target}")
                    self.stats.addCellPush()
                    self.stats.addCellMove()
                    self.memory.append((self.turnCount, "The Vengabus is Evolving O.o at signal {signal_at_target} (Move Bounced)", (new_x, new_y)))
                    if not self.alive:
                        self.environment.addInertAt(self.x, self.y, CELL_DEATH_RELEASE_INERT)
                return True
                    
        print(f"IDK WHAT'S HERE: {cell} at signal {signal_at_target}")
        self.memory.append((self.turnCount, "IDK WHAT'S HERE: {cell} at signal {signal_at_target}", {signal_at_target}))
        return True
        
    def move(self):
        if not self.alive or self.energy < CELL_MOVE_ENERGY_MIN:
            self.memory.append((self.turnCount, "had a lie in today", self.energy))
            self.stats.addCellStop()
            # print(f"Not moving because alive is {self.alive} & energy is {self.energy}")
            return
        
        # Movement based on environmental signals and nutrient concentration
        potentialMoves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(potentialMoves)
        blockCounter = 0
        maxMoveAttempts = 4

        while blockCounter < maxMoveAttempts:
            bestMove = None
            maxSignal = -1
            for dx, dy in potentialMoves:
                # print(f"Considering move ({dx},{dy})")
                new_x = (self.x + dx) % self.environment.grid.shape[0]
                new_y = (self.y + dy) % self.environment.grid.shape[1]
                signal = self.environment.signalGrid[new_x, new_y]
                self.memory.append((self.turnCount, "Considered another direction", ({dx},{dy})))
                # print(f"env: {lightGrid[new_x, new_y]} wai: {waifuGrid[new_x, new_y]} per: {self.perception_strength}")
                if signal > maxSignal and self.environment.canAddCellAt(new_x, new_y):
                    # print(f"Best signal")
                    bestMove = (dx, dy)
                    maxSignal = signal
            if bestMove:
                bestMove = (dx, dy)
                new_x = (self.x + dx) % self.environment.grid.shape[0]
                new_y = (self.y + dy) % self.environment.grid.shape[1]
                self.environment.moveCellTo(new_x, new_y, self)
                self.stats.addCellMove()
                self.memory.append((self.turnCount, f"Moved to signal {maxSignal}", (new_x, new_y)))
            
            else:
                blockCounter += 1
                self.memory.append((self.turnCount, f"You're really gonna block me {blockCounter} time(s)?", (self.x, self.y)))

            if self.resilience > self.environment.grid[new_x,new_y].resilience:
                # Current cell resilience sup to target resilience
                # Try to push the target away
                # print(f"Squish time")
                self.environment.grid[new_x,new_y].moveOrSquish(self, (dx, dy))
                self.memory.append((self.turnCount, "did he die!?", {self.resilience}))
                self.energy = random.uniform(0.8, 1.1) * self.energy
                self.memory.append((self.turnCount, "wait, huh?!", {self.energy}))
        
                if self.x != new_x or self.y != new_y:
                    print(f"Failed moving {self.id} from ({self.x}, {self.y}) to ({new_x}, {new_y})")
                    self.memory.append((self.turnCount, "Move Failed", (new_x, new_y)))
                else:
                    print(f"Failed moving {self.id} onto itself")
                    self.memory.append((self.turnCount, "Move Failed", (new_x, new_y)))
        
    def getCellColor(self):
        if self.organism:
            if self.organism.name: # sentient = random color picked once
                if not hasattr(self.organism, "color"):
                    self.organism.color = hsv_to_rgb((random.uniform(0, 1), min(1, max(0.8, self.energy / self.topEnergy)), min(max(0.5, self.energy / self.topEnergy), 1)))
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
            nutrientAbsorptionValue = nutrients * self.growthRate
            self.energy += nutrientAbsorptionValue
            self.environment.depleteLightAt(self.x, self.y, (nutrientAbsorptionValue * ENVIRONMENT_LIGHT_ABSORPTION_WASTE))
            self.memory.append((self.turnCount, "Gained Light Energy", nutrientAbsorptionValue))
            print(f"Turn {self.turnCount}: Cell {self.id} gained {nutrientAbsorptionValue} energy. Total: {self.energy}")
            # self.environment.lightGrid[self.x, self.y] = max(self.environment.lightGrid[self.x, self.y] - 0.02, 0)  # Deplete nutrients

    def emitLight(self):
        if self.state == "plasma": # Plasma cells consistently emit high light
            self.lightEmission = 5
            self.topEnergy = self.topEnergy - (self.topEnergy * CELL_LIGHT_EMISSION_ENERGY_COST_MULTIPLIER)
            self.memory.append((self.turnCount, "Emitted light", (self.lightEmission)))
            # lightGrid[self.x, self.y] = min(lightGrid[self.x, self.y] + self.light_emission, 100)
        elif random.random() < 0.01 and self.energy > self.fertilityEnergyMin: # Non-plasma cells have a random chance to emit light
            self.lightEmission = 1
            self.memory.append((self.turnCount, "Suddenly emitted light?!", (self.lightEmission)))
            self.lightEmission = 0
            # lightGrid[self.x, self.y] = min(lightGrid[self.x, self.y] + self.light_emission, 100)
        else:
            self.lightEmission = 0
        self.environment.addLightAt(self.x, self.y, self.lightEmission)
            
    def waifuSignal(self):
        if self.alive:
            self.environment.addAttractivenessAt(self.x, self.y, self.attractiveness)
            # waifuGrid[self.x, self.y] = min(waifuGrid[self.x, self.y] + self.attractiveness, 100)
            vibes = self.environment.getAttractivenessAt(self.x, self.y) # waifuGrid[self.x, self.y]
            attractivenessGain = vibes * self.growthRate * (CELL_ATTRACTIVENESS_GAIN_MODIFIER/50)
            self.attractiveness += attractivenessGain
            self.memory.append((self.turnCount, "DAT ASS GAINED ATTRACTIVENESS", {attractivenessGain}))
        else:
            self.environment.setAttractivenessAt(self.x, self.y, 0)
            # waifuGrid[self.x, self.y] = 0
            self.memory.append((self.turnCount, "Even my death turns people off!?", 0))

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
            if not hasattr(self, "state") or self.state != "plasma":
                self.state = "plasma"
                self.hue = random.uniform(CELL_STATE_PLASMA_COLOR_MIN, CELL_STATE_PLASMA_COLOR_MAX)
                self.alpha = random.uniform(CELL_STATE_PLASMA_ALPHA_MIN, CELL_STATE_PLASMA_ALPHA_MAX)
                self.stats.addCellStateChange("plasma")
                self.memory.append((self.turnCount, "Became Plasma", 0))
            else:
                self.stats.addCellStateStable()
        elif CELL_STATE_GAS_ENERGY < self.energy <= CELL_STATE_PLASMA_ENERGY:
            if not hasattr(self, "state") or self.state != "gas":
                self.state = "gas"
                self.hue = random.uniform(CELL_STATE_GAS_COLOR_MIN, CELL_STATE_GAS_COLOR_MAX)
                self.alpha = random.uniform(CELL_STATE_GAS_ALPHA_MIN, CELL_STATE_GAS_ALPHA_MAX)
                self.stats.addCellStateChange("gas")
                self.memory.append((self.turnCount, "Became Gas", 0))
            else:
                self.stats.addCellStateStable()
        elif CELL_STATE_LIQUID_ENERGY < self.energy <= CELL_STATE_GAS_ENERGY:
            if not hasattr(self, "state") or self.state != "liquid":
                self.state = "liquid"
                self.hue = random.uniform(CELL_STATE_LIQUID_COLOR_MIN, CELL_STATE_LIQUID_COLOR_MAX)
                self.alpha = random.uniform(CELL_STATE_LIQUID_ALPHA_MIN, CELL_STATE_LIQUID_ALPHA_MAX)
                self.stats.addCellStateChange("liquid")
                self.memory.append((self.turnCount, "Became Liquid", 0))
            else:
                self.stats.addCellStateStable()
        elif CELL_STATE_MESOPHASE_ENERGY < self.energy <= CELL_STATE_LIQUID_ENERGY:
            if not hasattr(self, "state") or self.state != "mesophase":
                self.state = "mesophase"
                self.hue = random.uniform(CELL_STATE_MESOPHASE_COLOR_MIN, CELL_STATE_MESOPHASE_COLOR_MAX)
                self.alpha = random.uniform(CELL_STATE_MESOPHASE_ALPHA_MIN, CELL_STATE_MESOPHASE_ALPHA_MAX)
                self.stats.addCellStateChange("mesophase")
                self.memory.append((self.turnCount, "Entered the Mesophase", 0))
            else:
                self.stats.addCellStateStable()
        elif CELL_STATE_SOLID_ENERGY < self.energy <= CELL_STATE_MESOPHASE_ENERGY:
            if not hasattr(self, "state") or self.state != "solid":
                self.state = "solid"
                self.hue = random.uniform(CELL_STATE_SOLID_COLOR_MIN, CELL_STATE_SOLID_COLOR_MAX)
                self.alpha = random.uniform(CELL_STATE_SOLID_ALPHA_MIN, CELL_STATE_SOLID_ALPHA_MAX)
                self.stats.addCellStateChange("solid")
                self.memory.append((self.turnCount, "Got Hard", 0))
            else:
                self.stats.addCellStateStable()
        elif CELL_STATE_INERT_ENERGY < self.energy <= CELL_STATE_SOLID_ENERGY:
            if not hasattr(self, "state") or self.state != "inert" :
                self.state = "inert"
                self.hue = self.hue if hasattr(self, "hue") else random.uniform(CELL_STATE_INERT_COLOR_MIN, CELL_STATE_INERT_COLOR_MAX)
                self.alpha = CELL_STATE_INERT_ALPHA_MIN
                self.stats.addCellStateChange("inert")
                self.memory.append((self.turnCount, "Became Inert", 0))
            else:
                self.stats.addCellStateStable()

    def reproduce(self):
        if not self.alive:
            return False
        if self.age > self.fertilityAgeMax:
            self.stats.addCellElderly()
            return False
        if self.age < self.fertilityAgeMin:
            self.stats.addCellYouth()
            return False
        self.stats.addCellAdult()
        if self.energy < self.fertilityEnergyMin:
            self.stats.addCellBabyFailed("Exhausted")
            self.memory.append((self.turnCount, "Too lazy to fuck", 0))
            return False
        # reproducing a cell inside an organism (will be done in organism)
        #if self.organism is not None:
        #    return False
        # Generate a baby cell if enough energy
        if (random.random()*100) < self.fertilityRate or (self.attractiveness > ((self.CellAttractivenessTopRecord/10)*9)):
            if self.state is "inert": # inert cells 'birth' enrichment onto environment
                enrichInert = min(self.age, self.mass)
                self.mass -= enrichInert
                self.environment.addInertAt(self.x, self.y, (enrichInert * 0.2)) # 20% at self, 10% at each adjacent
                self.environment.addInertAt(self.x + 1, self.y, (enrichInert * 0.1)) # Top
                self.environment.addInertAt(self.x, self.y + 1, (enrichInert * 0.1)) # Right
                self.environment.addInertAt(self.x - 1, self.y, (enrichInert * 0.1)) # Bottom
                self.environment.addInertAt(self.x, self.y - 1, (enrichInert * 0.1)) # Left
                self.stats.addCellDisintegration()
                self.memory.append((self.turnCount, "Enriched the earth", (enrichInert * 0.6)))
                if self.mass <= 0:
                    # disappear from board
                    self.environment.removeCellFromGrid(self)
                    self.stats.addCellDisintegrationDeath()
                    self.memory.append((self.turnCount, "Oop bye", 0))
            else: 
                x, y = (self.x + random.choice([-1, 1])) % self.environment.grid.shape[0], (self.y + random.choice([-1, 1])) % self.environment.grid.shape[1]
                if self.environment.canAddCellAt(x, y):  # Empty spot
                    self.energy = (self.energy/CELL_REPRODUCTION_SUCCESS_COST)
                    self.topEnergy = (self.topEnergy/CELL_REPRODUCTION_SUCCESS_COST)
                    baby_cell = Cell(x, y, self.stats, self.environment, organismCheck=None)
                    baby_cell.growthRate = max(0.5, min(2.0, self.growthRate + random.uniform(CELL_BABY_MUTATION_GROWTH_MIN, CELL_BABY_MUTATION_GROWTH_MAX)))
                    baby_cell.resilience = max(0.5, min(2.0, self.resilience + random.uniform(CELL_BABY_MUTATION_RESILIENCE_MIN, CELL_BABY_MUTATION_RESILIENCE_MAX)))
                    baby_cell.perceptionStrength = max(0.1, min(1.0, self.perceptionStrength + random.uniform(CELL_BABY_MUTATION_PERCEPTION_MIN, CELL_BABY_MUTATION_PERCEPTION_MAX)))
                    baby_cell.speed = max(0.5, min(2.0, self.speed + random.uniform(CELL_BABY_MUTATION_SPEED_MIN, CELL_BABY_MUTATION_SPEED_MAX)))
                    baby_cell.role = random.choice(CELL_ROLES)
                    self.environment.setCellAt(x, y, baby_cell)
                    # print("UNEBEBEEEEEEEEEEEEEEEEE!!!!!!!!!!!!!!!!!!1!!!!!!!!!!!!!1!!!")
                    if self.attractiveness < ((self.CellAttractivenessTopRecord/10)*9):
                        self.memory.append((self.turnCount, "Wait, une bebe?! Where did this thing come from!?", {self.fertilityRate}))
                        self.stats.addCellBaby("Fertile")
                        return True
                    else:
                        self.memory.append((self.turnCount, "Can't believe i'm finally a parent!", {self.attractiveness}))
                        self.stats.addCellBaby("Attractive")
                        return True
                else:
                    self.energy = (self.energy/CELL_REPRODUCTION_FAILURE_COST)
                    # print("Tried to UNEBEBEBEBEBEBEBEE BUT NO SPACE LEFT")
                    self.stats.addCellBabyFailed("Overpopulation")
                    self.memory.append((self.turnCount, "Didn't have room for even 1 bebe :(", 0))
                    return False
            return False

    def decay(self):
        if not self.alive:
            return
        self.energy -= random.uniform(0.95, 1.05) * (CELL_DECAY_ENERGY_MULTIPLIER * (((self.age - self.resilience) * self.speed)/100))  # Energy loss increases with speed
        self.age += CELL_DECAY_AGE_PER_TURN
        self.growthRate -= random.uniform(0.95, 1.05) * self.growthDecayRate
        self.lifeExpectancy = random.uniform(0.95, 1.05) * random.uniform(self.lifeExpectancyMin, self.lifeExpectancyMax)
        self.attractiveness = random.uniform(0.95, 1.05) * ((self.energy*(CELL_ATTRACTIVENESS_NORM_ENERGY))+(self.age*(CELL_ATTRACTIVENESS_NORM_AGE))+(self.growthRate*CELL_ATTRACTIVENESS_NORM_GROWTH)+(self.resilience*CELL_ATTRACTIVENESS_NORM_RESILIENCE)+(self.perceptionStrength*CELL_ATTRACTIVENESS_NORM_STRENGTH)+(self.speed*CELL_ATTRACTIVENESS_NORM_SPEED)+(self.lightEmission*CELL_ATTRACTIVENESS_NORM_LIGHT_EMISSION))/7
        if self.attractiveness > self.CellAttractivenessTopRecord:
            self.CellAttractivenessTopRecord = self.attractiveness
        if self.energy >= self.topEnergy * (random.uniform(0.9, 1.1) * CELL_DECAY_TOP_ENERGY_EXCESS):
            self.topEnergyDecay = self.topEnergy - ((self.topEnergy/10) * CELL_DECAY_TOP_ENERGY_MULTIPLIER)
            self.topEnergy = self.topEnergyDecay
            self.memory.append((self.turnCount, "Fuck, being this cool is too hard, I lost energy", [self.topEnergyDecay]))
            self.topEnergyDecay = 0
        #print(f"Rated {self.attractiveness}% hot")
        self.memory.append((self.turnCount, "I'm really rated this hot!?", {self.attractiveness}))
        if (self.energy <= 0) or (self.age > self.lifeExpectancy):  # Death by starvation or old age
            self.alive = False
            self.memory.append((self.turnCount, "I either starved, or got old - can't tell.", 0))
            print(f"Died from state {self.state} Energy: {self.energy}, lost {(1 / self.resilience) * self.speed} this turn")
            if self.age < self.lifeExpectancy:
                self.stats.addCellDeath(CELL_DEATH_REASON_STARVATION)
            else:
                self.stats.addCellDeath(CELL_DEATH_REASON_AGE)
            #else:
            #    self.stats.addCellDeath(CELL_DEATH_REASON_STARVATION)
            self.energy = 0
            self.state = "inert"
            self.environment.addLightAt(self.x, self.y, CELL_DEATH_RELEASE_LIGHT)
            self.environment.addInertAt(self.x, self.y, CELL_DEATH_RELEASE_INERT)
            #lightGrid[self.x, self.y] += CELL_DEATH_RELEASE_LIGHT  # Dead cells release light for some reason
            #inertGrid[self.x, self.y] += CELL_DEATH_RELEASE_INERT # Drop inert resources onto inert grid

    def needTurn(self, turn):
        return self.turnCount < turn
    
    def summarizeMemory(self):
        if self.alive == True:
            self.previousAlive = True
            return
        if self.alive == False and self.previousAlive == True:
            self.previousAlive = False
            summary = f"Cell {self.id} Summary (Total Memories: {len(self.memory)}):\n"
            memoryCounts = {}

            for (self.turnCount), memoryType, _ in self.memory:
                if memoryType not in memoryCounts:
                    memoryCounts[memoryType] = 0
                memoryCounts[memoryType] += 1

            for memoryType, count in memoryCounts.items():
                summary += f"- {memoryType}: {count}\n"
            
            print(f"{summary}")


    def runLoop(self, turn):
        self.turnCount = turn
        self.move()
        self.absorbNutrients()
        if self.energy > self.topEnergy:
            self.topEnergy = self.energy
        self.phaseTransition()
        self.reproduce()
        self.decay()
        self.waifuSignal()
        self.summarizeMemory()

