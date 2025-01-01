# CONFIG FILE: GAME OF WHY
# CHARIS CAT 2024

from datetime import datetime
from enum import Enum
import random
from matplotlib.colors import LinearSegmentedColormap


# ENVIRONMENT SIMULATION SETTINGS #
GRID_SIZE = 100
NUM_STEPS = 100000
CELL_BASE_COUNT = 10000 #50

class CellState(Enum):
    PLASMA = "plasma"
    GAS = "gas"
    LIQUID = "liquid"
    MESOPHASE = "mesophase"
    SOLID = "solid"
    INERT = "inert"

# phase transition boundaries
CELL_STATE_PLASMA_ENERGY = 250
CELL_STATE_GAS_ENERGY = 160
CELL_STATE_LIQUID_ENERGY = 60
CELL_STATE_MESOPHASE_ENERGY = 25
CELL_STATE_SOLID_ENERGY = 10
CELL_STATE_INERT_ENERGY = 0

CELL_STATE_PLASMA_COLOR_MIN = 0.0
CELL_STATE_PLASMA_COLOR_MAX = 0.1
CELL_STATE_GAS_COLOR_MIN = 0.7
CELL_STATE_GAS_COLOR_MAX = 0.75
CELL_STATE_LIQUID_COLOR_MIN = 0.5
CELL_STATE_LIQUID_COLOR_MAX = 0.7
CELL_STATE_SOLID_COLOR_MIN = 0.15
CELL_STATE_SOLID_COLOR_MAX = 0.35
CELL_STATE_MESOPHASE_COLOR_MIN = 0.8
CELL_STATE_MESOPHASE_COLOR_MAX = 1
CELL_STATE_INERT_COLOR_MIN = 0
CELL_STATE_INERT_COLOR_MAX = 0

CELL_STATE_PLASMA_ALPHA_MIN = 0.7
CELL_STATE_PLASMA_ALPHA_MAX = 0.95
CELL_STATE_GAS_ALPHA_MIN = 0.2
CELL_STATE_GAS_ALPHA_MAX = 0.4
CELL_STATE_LIQUID_ALPHA_MIN = 0.6
CELL_STATE_LIQUID_ALPHA_MAX = 0.9
CELL_STATE_MESOPHASE_ALPHA_MIN = 0.3
CELL_STATE_MESOPHASE_ALPHA_MAX = 1
CELL_STATE_SOLID_ALPHA_MIN = 1
CELL_STATE_SOLID_ALPHA_MAX = 1
CELL_STATE_INERT_ALPHA_MIN = 1

ORGANISM_STATE_SENTIENT_COLOR_MIN = 0
ORGANISM_STATE_SENTIENT_COLOR_MAX = 0
ORGANISM_STATE_SIMPLE_COLOR_MIN = 0
ORGANISM_STATE_SIMPLE_COLOR_MAX = 0

# environment settings
ENVIRONMENT_VISIBILITY_MULTIPLIER = 1 # raise or lower the amount of visual acuity for cells in the environment

# environmental enrichment settings
ENVIRONMENT_LIGHT_ENRICHMENT = 5000
ENVIRONMENT_LIGHT_ENRICHMENT_SOURCE_NUM = 500
ENVIRONMENT_LIGHT_ABSORPTION_WASTE = 1.2

# environmental decay settings
LIGHT_GRID_DECAY_RATE = 0.05
INERT_GRID_DECAY_RATE = 0.01
ATTRACTIVENESS_GRID_DECAY_RATE = 0.05

# light settings
ENVIRONMENT_LIGHT_CLIP_MIN = 0
ENVIRONMENT_LIGHT_CLIP_MAX = 10000

# attractiveness settings
ENVIRONMENT_ATTRACTIVENESS_CLIP_MIN = 0
ENVIRONMENT_ATTRACTIVENESS_CLIP_MAX = 100

# CELL SIMULATION SETTINGS #
CELL_ROLES = ["general", "structural", "sensory", "reproductive"]

# SPAWNED CELL STATS
CELL_BASE_ATTRACTIVENESS_MIN = 0

# energy
CELL_BASE_ENERGY_MIN = 0
CELL_BASE_ENERGY_MAX = 200

# growth rate
CELL_BASE_GROWTH_DECAY_RATE = 100 # Lost per turn: 100 is 1%, 50 is 50%, 0 is 100%, 1000 is 0.1%

CELL_BASE_GROWTH_RATE_MIN = 30
CELL_BASE_GROWTH_RATE_MAX = 70
CELL_PLASMA_GROWTH_RATE_MIN = 70
CELL_PLASMA_GROWTH_RATE_MAX = 100
CELL_GAS_GROWTH_RATE_MIN = 20
CELL_GAS_GROWTH_RATE_MAX = 50
CELL_LIQUID_GROWTH_RATE_MIN = 60
CELL_LIQUID_GROWTH_RATE_MAX = 90
CELL_MESOPHASE_GROWTH_RATE_MIN = 40
CELL_MESOPHASE_GROWTH_RATE_MAX = 70
CELL_SOLID_GROWTH_RATE_MIN = 10
CELL_SOLID_GROWTH_RATE_MAX = 40
CELL_INERT_GROWTH_RATE_MIN = 0
CELL_INERT_GROWTH_RATE_MAX = 1

# resilience
CELL_BASE_RESILIENCE_MIN = 30
CELL_BASE_RESILIENCE_MAX = 70 
CELL_PLASMA_RESILIENCE_MIN = 50
CELL_PLASMA_RESILIENCE_MAX = 70 
CELL_GAS_RESILIENCE_MIN = 10
CELL_GAS_RESILIENCE_MAX = 30 
CELL_LIQUID_RESILIENCE_MIN = 30
CELL_LIQUID_RESILIENCE_MAX = 50 
CELL_MESOPHASE_RESILIENCE_MIN = 40
CELL_MESOPHASE_RESILIENCE_MAX = 60 
CELL_SOLID_RESILIENCE_MIN = 60
CELL_SOLID_RESILIENCE_MAX = 100 
CELL_INERT_RESILIENCE_MIN = 80
CELL_INERT_RESILIENCE_MAX = 100 

# perception
CELL_BASE_PERCEPTION_MIN = 20
CELL_BASE_PERCEPTION_MAX = 50
CELL_PLASMA_PERCEPTION_MIN = 60
CELL_PLASMA_PERCEPTION_MAX = 90
CELL_GAS_PERCEPTION_MIN = 50
CELL_GAS_PERCEPTION_MAX = 80
CELL_LIQUID_PERCEPTION_MIN = 40
CELL_LIQUID_PERCEPTION_MAX = 70
CELL_MESOPHASE_PERCEPTION_MIN = 80
CELL_MESOPHASE_PERCEPTION_MAX = 100
CELL_SOLID_PERCEPTION_MIN = 5
CELL_SOLID_PERCEPTION_MAX = 15
CELL_INERT_PERCEPTION_MIN = 0
CELL_INERT_PERCEPTION_MAX = 5

# speed
CELL_BASE_SPEED_MIN = 40
CELL_BASE_SPEED_MAX = 80
CELL_PLASMA_SPEED_MIN = 90
CELL_PLASMA_SPEED_MAX = 100
CELL_GAS_SPEED_MIN = 80
CELL_GAS_SPEED_MAX = 100
CELL_LIQUID_SPEED_MIN = 50
CELL_LIQUID_SPEED_MAX = 100
CELL_MESOPHASE_SPEED_MIN = 20
CELL_MESOPHASE_SPEED_MAX = 70
CELL_SOLID_SPEED_MIN = 10
CELL_SOLID_SPEED_MAX = 25
CELL_INERT_SPEED_MIN = 0
CELL_INERT_SPEED_MAX = 10

# light absorption
CELL_BASE_LIGHT_ABSORPTION_MIN = 40*4
CELL_BASE_LIGHT_ABSORPTION_MAX = 70*4
CELL_PLASMA_LIGHT_ABSORPTION_MIN = 20*4
CELL_PLASMA_LIGHT_ABSORPTION_MAX = 40*4
CELL_GAS_LIGHT_ABSORPTION_MIN = 40*4
CELL_GAS_LIGHT_ABSORPTION_MAX = 60*4
CELL_LIQUID_LIGHT_ABSORPTION_MIN = 50*4
CELL_LIQUID_LIGHT_ABSORPTION_MAX = 70*4
CELL_MESOPHASE_LIGHT_ABSORPTION_MIN = 0*4
CELL_MESOPHASE_LIGHT_ABSORPTION_MAX = 100*4
CELL_SOLID_LIGHT_ABSORPTION_MIN = 20*4
CELL_SOLID_LIGHT_ABSORPTION_MAX = 40*4
CELL_INERT_LIGHT_ABSORPTION_MIN = 0*4
CELL_INERT_LIGHT_ABSORPTION_MAX = 10*4

# light emission
CELL_BASE_LIGHT_EMISSION_MIN = 0*4
CELL_BASE_LIGHT_EMISSION_MAX = 30*4
CELL_PLASMA_LIGHT_EMISSION_MIN = 70*4
CELL_PLASMA_LIGHT_EMISSION_MAX = 100*4
CELL_GAS_LIGHT_EMISSION_MIN = 20*4
CELL_GAS_LIGHT_EMISSION_MAX = 60*4
CELL_LIQUID_LIGHT_EMISSION_MIN = 5*4
CELL_LIQUID_LIGHT_EMISSION_MAX = 30*4
CELL_MESOPHASE_LIGHT_EMISSION_MIN = 0*4
CELL_MESOPHASE_LIGHT_EMISSION_MAX = 70*4
CELL_SOLID_LIGHT_EMISSION_MIN = 0*4
CELL_SOLID_LIGHT_EMISSION_MAX = 20*4
CELL_INERT_LIGHT_EMISSION_MIN = 0*4
CELL_INERT_LIGHT_EMISSION_MAX = 10*4

# life expectancy
CELL_BASE_DEATH_AGE_MIN = 80*4
CELL_BASE_DEATH_AGE_MAX = 500*4
CELL_PLASMA_DEATH_AGE_MIN = 80*4
CELL_PLASMA_DEATH_AGE_MAX = 500*4
CELL_GAS_DEATH_AGE_MIN = 80*4
CELL_GAS_DEATH_AGE_MAX = 500*4
CELL_LIQUID_DEATH_AGE_MIN = 80*4
CELL_LIQUID_DEATH_AGE_MAX = 500*4
CELL_MESOPHASE_DEATH_AGE_MIN = 80*4
CELL_MESOPHASE_DEATH_AGE_MAX = 500*4
CELL_SOLID_DEATH_AGE_MIN = 80*4
CELL_SOLID_DEATH_AGE_MAX = 500*4
CELL_INERT_DEATH_AGE_MIN = 80*4
CELL_INERT_DEATH_AGE_MAX = 500*4

# height
CELL_BASE_HEIGHT_MIN = 10
CELL_BASE_HEIGHT_MAX = 50
CELL_PLASMA_HEIGHT_MIN = 10
CELL_PLASMA_HEIGHT_MAX = 50
CELL_GAS_HEIGHT_MIN = 10
CELL_GAS_HEIGHT_MAX = 50
CELL_LIQUID_HEIGHT_MIN = 10
CELL_LIQUID_HEIGHT_MAX = 50
CELL_MESOPHASE_HEIGHT_MIN = 10
CELL_MESOPHASE_HEIGHT_MAX = 50
CELL_SOLID_HEIGHT_MIN = 10
CELL_SOLID_HEIGHT_MAX = 50
CELL_INERT_HEIGHT_MIN = 10
CELL_INERT_HEIGHT_MAX = 50

# mass
CELL_BASE_MASS_MIN = 10
CELL_BASE_MASS_MAX = 50
CELL_PLASMA_MASS_MIN = 10
CELL_PLASMA_MASS_MAX = 50
CELL_GAS_MASS_MIN = 10
CELL_GAS_MASS_MAX = 50
CELL_LIQUID_MASS_MIN = 10
CELL_LIQUID_MASS_MAX = 50
CELL_MESOPHASE_MASS_MIN = 10
CELL_MESOPHASE_MASS_MAX = 50
CELL_SOLID_MASS_MIN = 10
CELL_SOLID_MASS_MAX = 50
CELL_INERT_MASS_MIN = 10
CELL_INERT_MASS_MAX = 50

# reproduction values
CELL_BASE_MUTATION_RATE_MIN = 0
CELL_BASE_MUTATION_RATE_MAX = 100
CELL_PLASMA_MUTATION_RATE_MIN = 0
CELL_PLASMA_MUTATION_RATE_MAX = 100
CELL_GAS_MUTATION_RATE_MIN = 0
CELL_GAS_MUTATION_RATE_MAX = 100
CELL_LIQUID_MUTATION_RATE_MIN = 0
CELL_LIQUID_MUTATION_RATE_MAX = 100
CELL_MESOPHASE_MUTATION_RATE_MIN = 0
CELL_MESOPHASE_MUTATION_RATE_MAX = 100
CELL_SOLID_MUTATION_RATE_MIN = 0
CELL_SOLID_MUTATION_RATE_MAX = 100
CELL_INERT_MUTATION_RATE_MIN = 0
CELL_INERT_MUTATION_RATE_MAX = 100

# fertility age
CELL_BASE_FERTILITY_START_AGE_MIN = max(8, (random.uniform(0.9, 1.1) * CELL_BASE_DEATH_AGE_MIN/100))
CELL_BASE_FERTILITY_START_AGE_MAX = random.uniform(0.9, 1.1) * max(CELL_BASE_FERTILITY_START_AGE_MIN, CELL_BASE_DEATH_AGE_MIN)
CELL_BASE_FERTILITY_END_AGE_MIN = random.uniform(1,2) * CELL_BASE_FERTILITY_START_AGE_MAX
CELL_BASE_FERTILITY_END_AGE_MAX = random.uniform(CELL_BASE_DEATH_AGE_MIN, CELL_BASE_DEATH_AGE_MAX)
CELL_PLASMA_FERTILITY_START_AGE_MIN = max(8, (random.uniform(0.9, 1.1) * CELL_PLASMA_DEATH_AGE_MIN/100))
CELL_PLASMA_FERTILITY_START_AGE_MAX = random.uniform(0.9, 1.1) * max(CELL_PLASMA_FERTILITY_START_AGE_MIN, CELL_PLASMA_DEATH_AGE_MIN)
CELL_PLASMA_FERTILITY_END_AGE_MIN = random.uniform(1,2) * CELL_PLASMA_FERTILITY_START_AGE_MAX
CELL_PLASMA_FERTILITY_END_AGE_MAX = random.uniform(CELL_PLASMA_DEATH_AGE_MIN, CELL_PLASMA_DEATH_AGE_MAX)
CELL_GAS_FERTILITY_START_AGE_MIN = max(8, (random.uniform(0.9, 1.1) * CELL_GAS_DEATH_AGE_MIN/100))
CELL_GAS_FERTILITY_START_AGE_MAX = random.uniform(0.9, 1.1) * max(CELL_GAS_FERTILITY_START_AGE_MIN, CELL_GAS_DEATH_AGE_MIN)
CELL_GAS_FERTILITY_END_AGE_MIN = random.uniform(1,2) * CELL_GAS_FERTILITY_START_AGE_MAX
CELL_GAS_FERTILITY_END_AGE_MAX = random.uniform(CELL_GAS_DEATH_AGE_MIN, CELL_GAS_DEATH_AGE_MAX)
CELL_LIQUID_FERTILITY_START_AGE_MIN = max(8, (random.uniform(0.9, 1.1) * CELL_LIQUID_DEATH_AGE_MIN/100))
CELL_LIQUID_FERTILITY_START_AGE_MAX = random.uniform(0.9, 1.1) * max(CELL_LIQUID_FERTILITY_START_AGE_MIN, CELL_LIQUID_DEATH_AGE_MIN)
CELL_LIQUID_FERTILITY_END_AGE_MIN = random.uniform(1,2) * CELL_LIQUID_FERTILITY_START_AGE_MAX
CELL_LIQUID_FERTILITY_END_AGE_MAX = random.uniform(CELL_LIQUID_DEATH_AGE_MIN, CELL_LIQUID_DEATH_AGE_MAX)
CELL_MESOPHASE_FERTILITY_START_AGE_MIN = max(8, (random.uniform(0.9, 1.1) * CELL_MESOPHASE_DEATH_AGE_MIN/100))
CELL_MESOPHASE_FERTILITY_START_AGE_MAX = random.uniform(0.9, 1.1) * max(CELL_MESOPHASE_FERTILITY_START_AGE_MIN, CELL_MESOPHASE_DEATH_AGE_MIN)
CELL_MESOPHASE_FERTILITY_END_AGE_MIN = random.uniform(1,2) * CELL_MESOPHASE_FERTILITY_START_AGE_MAX
CELL_MESOPHASE_FERTILITY_END_AGE_MAX = random.uniform(CELL_MESOPHASE_DEATH_AGE_MIN, CELL_MESOPHASE_DEATH_AGE_MAX)
CELL_SOLID_FERTILITY_START_AGE_MIN = max(10, (random.uniform(0.9, 1.1) * CELL_SOLID_DEATH_AGE_MIN/100))
CELL_SOLID_FERTILITY_START_AGE_MAX = random.uniform(0.9, 1.1) * max(CELL_SOLID_FERTILITY_START_AGE_MIN, CELL_SOLID_DEATH_AGE_MIN)
CELL_SOLID_FERTILITY_END_AGE_MIN = random.uniform(1,2) * CELL_SOLID_FERTILITY_START_AGE_MAX
CELL_SOLID_FERTILITY_END_AGE_MAX = random.uniform(CELL_SOLID_DEATH_AGE_MIN, CELL_SOLID_DEATH_AGE_MAX)
CELL_INERT_FERTILITY_START_AGE_MIN = max(20, (random.uniform(0.9, 1.1) * CELL_INERT_DEATH_AGE_MIN/100))
CELL_INERT_FERTILITY_START_AGE_MAX = random.uniform(0.9, 1.1) * max(CELL_INERT_FERTILITY_START_AGE_MIN, CELL_INERT_DEATH_AGE_MIN)
CELL_INERT_FERTILITY_END_AGE_MIN = random.uniform(1,2) * CELL_INERT_FERTILITY_START_AGE_MAX
CELL_INERT_FERTILITY_END_AGE_MAX = random.uniform(CELL_INERT_DEATH_AGE_MIN, CELL_INERT_DEATH_AGE_MAX)

# min energy needed for bebeh
CELL_BASE_FERTILITY_ENERGY_MIN = 100
CELL_BASE_FERTILITY_ENERGY_MAX = 4000
CELL_PLASMA_FERTILITY_ENERGY_MIN = 200
CELL_PLASMA_FERTILITY_ENERGY_MAX = 4000
CELL_GAS_FERTILITY_ENERGY_MIN = 180
CELL_GAS_FERTILITY_ENERGY_MAX = 2300
CELL_LIQUID_FERTILITY_ENERGY_MIN = 110
CELL_LIQUID_FERTILITY_ENERGY_MAX = 1600
CELL_MESOPHASE_FERTILITY_ENERGY_MIN = 40
CELL_MESOPHASE_FERTILITY_ENERGY_MAX = 950
CELL_SOLID_FERTILITY_ENERGY_MIN = 15
CELL_SOLID_FERTILITY_ENERGY_MAX = 700
CELL_INERT_FERTILITY_ENERGY_MIN = 5
CELL_INERT_FERTILITY_ENERGY_MAX = 500

# fertility RATE
CELL_BASE_FERTILITY_RATE_MIN = 50
CELL_BASE_FERTILITY_RATE_MAX = 150
CELL_PLASMA_FERTILITY_RATE_MIN = 50
CELL_PLASMA_FERTILITY_RATE_MAX = 150
CELL_GAS_FERTILITY_RATE_MIN = 50
CELL_GAS_FERTILITY_RATE_MAX = 150
CELL_LIQUID_FERTILITY_RATE_MIN = 50
CELL_LIQUID_FERTILITY_RATE_MAX = 150
CELL_MESOPHASE_FERTILITY_RATE_MIN = 50
CELL_MESOPHASE_FERTILITY_RATE_MAX = 150
CELL_SOLID_FERTILITY_RATE_MIN = 50
CELL_SOLID_FERTILITY_RATE_MAX = 150
CELL_INERT_FERTILITY_RATE_MIN = 50
CELL_INERT_FERTILITY_RATE_MAX = 150

CELL_REPRODUCTION_FAILURE_COST = -0.1 
CELL_REPRODUCTION_SUCCESS_COST = 5 # multiplier for how much energy loss is incurred from reproducing
CELL_LIGHT_EMISSION_ENERGY_COST_MULTIPLIER = -1

CELL_BABY_MUTATION_GROWTH_MIN = -0.1
CELL_BABY_MUTATION_GROWTH_MAX = 0.1
CELL_BABY_MUTATION_RESILIENCE_MIN = -0.1
CELL_BABY_MUTATION_RESILIENCE_MAX = 0.1
CELL_BABY_MUTATION_SPEED_MIN = -0.05
CELL_BABY_MUTATION_SPEED_MAX = 0.05
CELL_BABY_MUTATION_PERCEPTION_MIN = -0.1
CELL_BABY_MUTATION_PERCEPTION_MAX = 0.1

# death values
CELL_DEATH_AGE_MIN = 80
CELL_DEATH_AGE_MAX = 500

CELL_DEATH_REASON_SQUISH = "squish"
CELL_DEATH_REASON_AGE = "age"
CELL_DEATH_REASON_STARVATION = "starvation"

CELL_DEATH_RELEASE_LIGHT = 0.5

CELL_DEATH_RELEASE_INERT = 200 # maybe make equivalent to the cells final weight, eventually
CELL_DEATH_RELEASE_INERT_MODIFIER = 100

CELL_DEATH_RELEASE_SQUISH_MIN = 0.2
CELL_DEATH_RELEASE_SQUISH_MAX = 0.6

CELL_DECAY_ENERGY_MULTIPLIER = 100 # Lost per turn: 100 is 1%, 50 is 50%, 0 is 100%, 1000 is 0.1%
CELL_DECAY_EXCESS_ENERGY_MULTIPLIER = 300 # Lost per turn when exceeding record energy: 100 is 1%, 50 is 50%, 0 is 100%, 1000 is 0.1%
CELL_DECAY_TOP_ENERGY_EXCESS = 1
CELL_DECAY_AGE_PER_TURN = 1

# social norms
CELL_ATTRACTIVENESS_NORM_ENERGY = 50
CELL_ATTRACTIVENESS_NORM_AGE = 50
CELL_ATTRACTIVENESS_NORM_GROWTH = 50
CELL_ATTRACTIVENESS_NORM_RESILIENCE = 50
CELL_ATTRACTIVENESS_NORM_PERCEPTION = 50
CELL_ATTRACTIVENESS_NORM_STRENGTH = 50
CELL_ATTRACTIVENESS_NORM_SPEED = 50
CELL_ATTRACTIVENESS_NORM_LIGHT_EMISSION = 50
CELL_ATTRACTIVENESS_NORM_MUTATION_RATE = 50
CELL_ATTRACTIVENESS_NORM_LIFE_EXPECTANCY = 50
CELL_ATTRACTIVENESS_NORM_MASS = 50
CELL_ATTRACTIVENESS_NORM_HEIGHT = 50
CELL_ATTRACTIVENESS_GAIN_MODIFIER = 50
CELL_ATTRACTIVENESS_TOP_RECORD_INIT = 50
CELL_ATTRACTIVENESS_IMPORTANCE_MODIFER = 50

# MOVEMENT SIMULATION SETTINGS #
CELL_MOVE_BLOCKED_MAX = 4
CELL_MOVE_ENERGY_MIN = 10

# VISUALISATION SETTINGS #
VISUALISATION_BASE_ENERGY_TOP_RECORD = 100
MAIN_GRID_IMPORTANCE = 1
INERT_GRID_TRANSPARENCY = 1
INERT_GRID_IMPORTANCE = 1.2
ATTRACTIVENESS_GRID_TRANSPARENCY = 0.5
ATTRACTIVENESS_GRID_IMPORTANCE = 1.3
LIGHT_GRID_TRANSPARENCY = 0.3
LIGHT_GRID_IMPORTANCE = 2

# Custom Colormaps
LIGHT_GRID_COLORMAP = LinearSegmentedColormap.from_list("lightGridColormap", [
    (0.0, (0, 0, 0, 0.2)),  # Black, fully opaque
    (0.4, (0.4, 0.3, 0.1, 0.15)),  # Dark brownish, less opaque
    (0.7, (0.8, 0.6, 0.2, 0.1)),  # Soft yellow, even more transparent
    (1.0, (1.0, 1.0, 0.9, 0.05)),  # Bright yellow-white, very transparent
])

INERT_GRID_COLORMAP = LinearSegmentedColormap.from_list("inertGridColormap", [
    (0, 0, 0, 0),      # transparent
    (0.1, 0.3, 0.1, 1),  # green
    (0.4, 0.3, 0.2, 1),  # brown
    (0.2, 0.2, 0.2, 1)   # grey
])

VISUALISATION_OUTPUT_FILE_SAVE_EVERY_N_TURNS = 100 # Save the main screen output as a file every N turns
VISUALISATION_OUTPUT_FILE_SAVE_FINAL_TURN = True # Save the final screen as a file
VISUALISATION_OUTPUT_FILE_SAVE_FORMAT = "png" # File format
VISUALISATION_OUTPUT_FILE_SAVE_MAIN_FOLDER = "visualisations"
VISUALISATION_OUTPUT_FILE_SAVE_SIM_FOLDER = f"{datetime.now().isoformat(timespec="seconds")}"
VISUALISATION_OUTPUT_SCREEN_DISABLE = False # Disable main screen output
VISUALISATION_OUTPUT_UPDATE_EVERY_N_TURN = 1 # Update the main screen output every N turns

CELL_MEMORY_DISPLAY_MODE = "event" # Display memory by event type (event) or turn order (turn) 
