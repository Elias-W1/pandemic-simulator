from random import randint

class Disease():
    def __init__(self, name, death_rate, infection_time, recovery_time, mutation_chance, infection_rate, parent=None):
        self.name = name
        self.death_rate = death_rate
        self.infection_rate = infection_rate
        self.infection_time = infection_time
        self.recovery_time = recovery_time
        self.mutation_chance = mutation_chance

        self.infection_count = 0

        print("New disease created: ", self.name)

    def mutate(self):
        #todo mutation factor CONSTANTS
        return Disease(self.get_mutation_name(), self.death_rate+0.02, self.infection_time+100, self.recovery_time,  self.mutation_chance+0.02, self.infection_rate, parent=self)


    def infect_particle(self, particle, tick):
        num = randint(0,100) / 100
        if num <= self.mutation_chance:
            new_disease = self.mutate()
            particle.infect_with(new_disease, tick)
            return new_disease
        else:
            particle.infect_with(self, tick)
            return None

    def add_infected(self):
        self.infection_count += 1

    def get_mutation_name(self):
        return self.name+" mutation_"+str(randint(2000,3000))

