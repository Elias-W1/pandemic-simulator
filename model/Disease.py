from model.Constants import *
from random import randint
import numpy as np
import random
import string

class Disease():
    def __init__(self, name, death_rate, infection_time, recovery_time, mutation_chance, infection_rate, mutations_enabled, parent=None, infection_count=0):
        self.name = name
        self.death_rate = death_rate
        self.infection_rate = infection_rate
        self.infection_time = infection_time
        self.recovery_time = recovery_time
        self.mutation_chance = mutation_chance
        self.mutations_enabled = mutations_enabled

        self.infection_count = infection_count

        self.active = True

        self.parent = parent
        self.children = [] # diseases directly mutated from this disease

        self.vaccine_ready = False

    def mutate(self):
        death_rate = max(min(round(np.random.normal(self.death_rate, DEATH_RATE_STANDARD_DEVIATION), 2), 1), 0)
        infection_time = max(round(np.random.normal(self.infection_time, INFECTION_TIME_STANDARD_DEVIATION)), 0)
        recovery_time = max(round(np.random.normal(self.recovery_time, RECOVERED_TIME_STANDARD_DEVIATION)), 0)
        mutation_chance = max(min(round(np.random.normal(self.mutation_chance, MUTATION_CHANCE_STANARD_DEVIATION),2), 1), 0)
        infection_rate = max(min(round(np.random.normal(self.infection_rate, INFECTION_RATE_STANDARD_DEVIATION),2), 1), 0)
        newdisease = Disease(self.get_mutation_name(), death_rate, infection_time, recovery_time,  mutation_chance, infection_rate, self.mutations_enabled, parent=self)
        self.children.append(newdisease)
        return newdisease


    def infect_particle(self, particle, tick):
        num = randint(0,100) / 100
        if (num <= self.mutation_chance) and self.mutations_enabled and self.mutation_chance > 0:
            new_disease = self.mutate()
            particle.infect_with(new_disease, tick)
            return new_disease
        else:
            particle.infect_with(self, tick)
            return None

    def add_infected(self):
        self.infection_count += 1

    def remove_infected(self):
        self.infection_count -= 1
        if self.infection_count < 1:
            self.active = False

    def get_mutation_name(self):
        end_string = str("".join(random.choices(string.ascii_uppercase + string.digits, k=MUTATION_END_STRING_LENGTH)))
        if self.parent == None: # If disease is initial disease then only return string with end_string attached.
            return self.name+"-"+end_string
        else:                   # Else remove previous end_string from disease name and add new end_string.
            split = self.name.split("-")
            newname = split[0]
            for i in range(1, len(split)-1): newname = newname+"-"+str(split[i])    # add split up parts if initial disease name contains -.
            newname = newname+"-"+end_string
            return newname

    def calculate_percentage_difference(self, disease):
        """Calculates attribute difference percentage of self and given disease."""
        death_rate_diff = abs(self.death_rate - disease.death_rate)
        if self.infection_time == 0:
            infection_time_diff = 1
        else:
            infection_time_diff = abs(1 - (disease.infection_time / self.infection_time))
        if self.recovery_time == 0:
            recovery_time_diff = 1
        else:
            recovery_time_diff = abs(1 - (disease.recovery_time / self.recovery_time))
        mutation_chance_diff = abs(self.mutation_chance - disease.mutation_chance)
        infection_rate_diff  = abs(self.infection_rate - disease.infection_rate)
        sum = death_rate_diff + infection_time_diff + recovery_time_diff + mutation_chance_diff + infection_rate_diff
        return sum





