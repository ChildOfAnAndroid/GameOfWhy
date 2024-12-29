# CELL CLASS FILE: GAME OF WHY
# CHARIS CAT 2024

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