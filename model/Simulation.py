import random
from random import randint
from model.Particle import *
from model.Statistics import *
from model.Disease import *
from model.Constants import *
from model.Target import *
from model.VaccineCenter import *
from model.Vaccine import *

def get_reversed(listobj):
    newlist = list(listobj).copy()
    newlist.reverse()
    return newlist



class Simulation():
    def __init__(self, startdisease_name, particle_count, infected_count, infection_rate, death_rate, infection_time, recovery_time, mutations_enabled, mutation_chance, x_border, y_border, particle_size):
        self.infected_count = infected_count
        self.particle_count = particle_count
        self.healthy_count = particle_count - infected_count
        self.dead_count = 0
        self.recovered_count = 0


        self.particle_size = particle_size
        self.infection_radius = DEFAULT_INFECTION_RADIUS

        self.initial_disease = Disease(startdisease_name, death_rate, infection_time, recovery_time, mutation_chance, infection_rate, mutations_enabled, parent=None, infection_count=self.infected_count)


        self.x_border = x_border
        self.y_border = y_border
        self.particles = []
        self.tick_counter = 0

        self.diseases = []
        self.diseases.append(self.initial_disease)

        self.statistics = Statistics(self.particle_count, self.infected_count)
        self.create_particles()

        self.masks = False
        self.sd = False
        self.vaccines_enabled = False
        self.center_count = DEFAULT_VACCINE_CENTER_COUNT
        self.vaccine_effective_percentage_difference = DEFAULT_DISEASE_DIFFERENCE_EFFECTIVENESS
        self.vaccine_research_time = DEFAULT_RESEARCH_TIME
        self.vaccine_restock = RESTOCK_TIME
        self.vaccine_centers = []
        self.vaccines = []

        self.targets = []

    def set_dimensions(self, width, height):
        self.x_border = width
        self.y_border = height
        for particle in self.particles:
            particle.x_border = self.x_border
            particle.y_border = self.y_border


    def create_particles(self):
        # Calculate maximum particle count without constantly overlapping particles. Don't start simulation when too many particles.
        maximum = self.get_maximum_particle_count()

        if self.particle_count > maximum:
            self.particle_count = maximum

        # Make randomly scrambled list with infected/healthy status strings to randomize positions of infected and healthy particles later.
        particles = [Status.INFECTED]*self.infected_count
        particles.extend([Status.HEALTHY]*(self.particle_count-self.infected_count))
        random.shuffle(particles)

        # Get random positions for particles. If random position is occupied, then  find next free position (cyclical).
        abssize = self.particle_size * 2 + 1
        particles_per_row = (self.x_border // abssize) // 2
        rows_maximum = (self.y_border // abssize) // 2

        x_list = [False] * particles_per_row
        positions = []  # 2d array to check wether position is occupied.
        for i in range(rows_maximum):
            positions.append(x_list.copy())
        

        for i in range(len(particles)):
            x = randint(0, particles_per_row-1)
            y = randint(0, rows_maximum-1)
            while positions[y][x] == True:
                x += 1
                if x > particles_per_row-1:
                    y += 1
                    x = 0
                if y > rows_maximum-1:
                    y = 0

            status = particles[i]
            positions[y][x] = True

            self.create_particle(status, abssize * x * 2 , self.y_border - (abssize * y * 2)  )


    def get_maximum_particle_count(self):
        abssize = self.particle_size * 2 + 1
        particles_per_row = (self.x_border // abssize) // 2
        rows_maximum = (self.y_border // abssize) // 2
        rows = self.particle_count // particles_per_row
        if self.particle_count % particles_per_row > 0:
            rows = rows + 1
        max = particles_per_row * rows_maximum - 1
        return max

    def set_infected_count(self, newcount):
        self.infected_count = newcount

    def create_particle(self, status, startx, starty):
        moving_dirs = [-1,1]
        particle = Particle(status, startx, starty, self.x_border, self.y_border,random.choice(moving_dirs), random.choice(moving_dirs), self.infection_radius, self.initial_disease, DEFAULT_PARTICLE_SIZE//2)
        if status == Status.INFECTED:
            particle.set_status_infected(self.tick_counter)
        self.particles.append(particle)

    def particle_routine(self):
        collided_particles = []
        for particle in self.particles:
            # check for particle collisions and adjust movement
            for particle_b in self.particles:
                pair = [particle, particle_b]
                if particle == particle_b or get_reversed(pair) in collided_particles or (particle.status == Status.DEAD or particle_b.status == Status.DEAD):
                    continue

                particle.reset_outline(self.tick_counter)

                collision_values = particle.collides_with(particle_b, self.tick_counter)
                # if collision update infected count, skip collided particle pair in second loop walkthrough and if new disease mutated add it to list of diseases
                self.infected_count += collision_values["new_infections"]

                if collision_values["collision"]:
                    collided_particles.append(pair)
                elif collision_values["sd_collision"]:
                    collided_particles.append(pair)

                if collision_values["new_disease"] != None:
                    newdisease = collision_values["new_disease"]
                    self.diseases.append(newdisease)
                    if self.vaccines_enabled:
                        vaccine = self.add_vaccine(newdisease)
                        for center in self.vaccine_centers:
                            center.add_vaccine(vaccine)



            # check for wall collisions and adjust movement accordingly
            particle.move()

            # update status of particle and counts of each status in simulation
            dead, recovered, healthy = particle.update_status(self.tick_counter)
            self.dead_count += dead
            self.recovered_count += recovered
            self.infected_count -= (dead+recovered)
            self.recovered_count -= healthy

    def add_vaccine(self, disease):
        vaccine = Vaccine(self.research_time, disease, self.vaccine_effective_percentage_difference)
        self.vaccines.append(vaccine)
        return vaccine


    def set_measures(self, parameters):
        # Social distancing measure.
        sd = parameters["social_distancing"]
        sd_count = parameters["social_distancing_count"]

        if sd_count == None:
            sd_count = int((parameters["social_distancing_percentage"] / 100) * self.particle_count)

        if self.sd == False and sd:
            self.distance_particles(sd_count)
        elif self.sd == True and sd == False:
            self.undistance_particles()
        self.sd = sd


        # Mask measure.
        masks = parameters["mask"]
        masked_count = parameters["masked_count"]
        if masked_count == None:
            masked_count = int((parameters["masked_percentage"] / 100) *self.particle_count)

        # masks parameter can be updated live
        if self.masks == False and masks:
            self.mask_particles(masked_count)
        elif self.masks == True and masks == False:
            self.unmask_particles()

        self.masks = masks

        # Vaccines.
        vaccines_enabled = parameters["vaccines"]
        self.center_count = parameters["center_count"]
        self.research_time = parameters["research_time"]
        self.vaccine_effective_percentage_difference = parameters["difference_percentage"]
        self.vaccine_center_capacity = parameters["capacity"]
        self.vaccine_restock = parameters["restock_per_day"]
        if self.vaccines_enabled == False and vaccines_enabled:
            self.enable_vaccines()
        elif self.vaccines_enabled == True and vaccines_enabled == False:
            self.disable_vaccines()

        self.vaccines_enabled = vaccines_enabled

    def enable_vaccines(self):
        # Randomly generate non-overlapping positions for vaccine centers.
        centers_per_row = (self.x_border // VACCINE_CENTER_SIZE) // 2
        row_maximum = (self.y_border // VACCINE_CENTER_SIZE) // 2

        x_list = [False] * centers_per_row
        positions = []  # 2d array to check wether position is occupied.
        for i in range(row_maximum):
            positions.append(x_list.copy())

        for i in range(self.center_count):
            x = randint(0, centers_per_row - 1)
            y = randint(0, row_maximum - 1)
            while positions[y][x] == True:
                x += 1
                if x > centers_per_row - 1:
                    y += 1
                    x = 0
                if y > row_maximum - 1:
                    y = 0
            positions[y][x] = True

            c = VaccineCenter(VACCINE_CENTER_SIZE * x, self.y_border - (VACCINE_CENTER_SIZE * y), self.vaccine_center_capacity, self.vaccine_restock)
            c.restock()
            self.vaccine_centers.append(c)

        for disease in self.diseases:
            self.add_vaccine(disease)

        self.targets.extend(self.vaccine_centers)

    def disable_vaccines(self):
        self.vaccines_enbaled = False
        for center in self.vaccine_centers:
            center.destroy()
        self.vaccine_centers = []
        self.vaccines = []

    def mask_particles(self, count):
        to_mask = random.sample(self.particles, count)
        for particle in to_mask:
            particle.mask()

    def unmask_particles(self):
        for particle in self.particles:
            particle.unmask()

    def distance_particles(self, count):
        to_distance = random.sample(self.particles, count)
        for particle in to_distance:
            particle.enable_social_distancing()

    def undistance_particles(self):
        for particle in self.particles:
            particle.sd = False

    def change_stepsize(self, newstepsize):
        for particle in self.particles:
            particle.stepsize_multiplier = newstepsize
            if particle.x_movement < 0 or particle.x_movement > 0:
                particle.x_movement = particle.x_movement / abs(particle.x_movement) * newstepsize

            if particle.y_movement < 0 or particle.y_movement > 0:
                particle.y_movement = particle.y_movement / abs(particle.y_movement) * newstepsize

    def set_movement(self, movement):
        for particle in self.particles:
                particle.movement = movement

    def tick(self):
        self.particle_routine()
        if self.vaccines_enabled:
            self.research_vaccines()
            self.vaccine_center_routine()

        self.tick_counter += 1
        self.healthy_count = self.particle_count - self.infected_count - self.dead_count - self.recovered_count
        self.statistics.add_data(self.healthy_count, self.infected_count, self.recovered_count, self.dead_count)

    def research_vaccines(self):
        for i in range(len(self.vaccines)):
            vaccine = self.vaccines[i]
            if vaccine.remaining_research_duration > 0:
                vaccine.remaining_research_duration -= 1
            elif vaccine.remaining_research_duration == 0 and vaccine.researched == False:
                vaccine.finish_research()

    def vaccine_center_routine(self):
        for center in self.vaccine_centers:
            center.refresh_stock(self.tick_counter)
            for a in range(len(center.vaccine_count_list)):
                vaccine, unassigned_count = center.vaccine_count_list[a]

                # Get particles which will be going to vaccine center.
                unassigned_particles = []
                for particle in self.particles:
                    if particle.assigned_vaccine == None and particle.status != Status.DEAD and (not vaccine.against_disease in particle.immunities):
                        unassigned_particles.append(particle)

                visiting_particles_count = min(unassigned_count, center.unassigned_vaccines_count, len(self.particles), len(unassigned_particles))
                visiting_particles = random.sample(unassigned_particles, visiting_particles_count)

                # Set particle target to vaccine station
                for particle in visiting_particles:
                    particle.assigned_vaccine = vaccine
                    particle.set_target(center)
            center.unassigned_vaccines_count = 0

    def get_status_counts(self):
        return self.healthy_count, self.infected_count, self.recovered_count, self.dead_count

    def get_tick(self):
        return self.tick_counter

    def destroy_targets(self):
        for target in self.targets:
            target.destroy()
        self.targets = []