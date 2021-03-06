from model.Movement import *
from model.Status import *

DEFAULT_DISEASE_NAME = "SarsCov19"

DEFAULT_PARTICLE_SIZE = 10
DEFAULT_PARTICLE_COUNT = 50
DEFAULT_INFECTED_COUNT = 1
DEFAULT_INFECTION_RATE = 1
DEFAULT_DEATH_RATE = 0.03
MASK_INFECTION_REDUCTION = 0.65
MASK_RADIUS_REDUCTION = 0.25
DEFAULT_INFECTION_TIME = 500
DEFAULT_RECOVERED_TIME = 300

DEFAULT_INFECTION_RADIUS = 4

SOCIAL_DISTANCING_RADIUS_MULTIPLIER = 4

DEFAULT_TARGET_WAITING_DURATION = 180
DEFAULT_VISITING_COUNT = 2

DEFAULT_MUTATION_CHANCE = 0.01
# mutations
DEATH_RATE_STANDARD_DEVIATION = 0.01
INFECTION_TIME_STANDARD_DEVIATION = 90
RECOVERED_TIME_STANDARD_DEVIATION = 60
MUTATION_CHANCE_STANARD_DEVIATION = 0.005
INFECTION_RATE_STANDARD_DEVIATION = 0.02

MUTATION_END_STRING_LENGTH = 5

# vaccines
DEFAULT_VACCINE_CENTER_COUNT = 3
DEFAULT_RESEARCH_TIME = 180
DEFAULT_DISEASE_DIFFERENCE_EFFECTIVENESS = 0.5
DEFAULT_VACCINE_CENTER_CAPACITY = 5
RESTOCK_TIME = 900

VACCINE_CENTER_SIZE = 15

OUTLINED_DURATION_TICKS = 10 # Defines how many ticks one particle should be outlined.

TICKS_IN_A_DAY = 60