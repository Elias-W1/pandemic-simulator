import random
from random import randint
from model.Particle import *
from model.Statistics import *
from model.Disease import *
from model.Constants import *
from model.Target import *

def get_reversed(listobj):
    newlist = list(listobj).copy()
    newlist.reverse()
    return newlist



class Simulation():
    def __init__(self, particle_count, infected_count, infection_rate, death_rate, infection_time, recovery_time, particle_size):
        self.infected_count = infected_count
        self.particle_count = particle_count
        self.healthy_count = particle_count - infected_count
        self.dead_count = 0
        self.recovered_count = 0

        self.particle_size = particle_size
        self.infection_radius = 3


        self.initial_disease = Disease("StartDisease", death_rate, infection_time, recovery_time, 0.01, infection_rate)


        self.x_border = 600
        self.y_border = 600
        self.particles = []
        self.tick_counter = 0

        self.diseases = []

        self.statistics = Statistics(self.particle_count, self.infected_count)
        self.create_particles()

        self.masks = False
        self.sd = False

        self.targets = []

    def create_particles(self):
        # Calculate maximum particle count without constantly overlapping particles. Don't start simulation when too many particles.
        maximum = self.get_maximum_particle_count()

        if self.particle_count > maximum:
            print("Maximum particle count exceeded. Max: ",maximum, " Particle Count: ",self.particle_count,"Not starting")
            return None

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
        

        print(len(positions), len(positions[0]))
        for i in range(len(particles)):
            x = randint(0, particles_per_row-1)
            y = randint(0, rows_maximum-1)
            while positions[y][x] == True:
                # print("Checking ",y,",",x,": ", positions[y][x])
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
        particle = Particle(status, startx, starty, random.choice(moving_dirs), random.choice(moving_dirs), self.infection_radius, self.initial_disease)
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
                    self.diseases.append(collision_values["new_disease"])


            # check for wall collisions and adjust movement accordingly
            particle.move()

            # update status of particle and counts of each status in simulation
            dead, recovered, healthy = particle.update_status(self.tick_counter)
            self.dead_count += dead
            self.recovered_count += recovered
            self.infected_count -= (dead+recovered)
            self.recovered_count -= healthy


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
            print("Masked count from percentage:", int(masked_count))

        # masks parameter can be updated live
        if self.masks == False and masks:
            self.mask_particles(masked_count)
        elif self.masks == True and masks == False:
            self.unmask_particles()

        self.masks = masks


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
            particle.x_movement = particle.x_movement / abs(particle.x_movement) * newstepsize
            particle.y_movement = particle.y_movement / abs(particle.y_movement) * newstepsize

    def set_movement(self, movement):
        if movement != Movement.DIRECTED:
            self.destroy_targets()
            for particle in self.particles:
                particle.movement = movement


    def tick(self):
        self.particle_routine()
        self.tick_counter += 1
        self.healthy_count = self.particle_count - self.infected_count - self.dead_count - self.recovered_count
        self.statistics.add_data(self.healthy_count, self.infected_count, self.recovered_count, self.dead_count)

    def get_status_counts(self):
        return self.healthy_count, self.infected_count, self.recovered_count, self.dead_count

    def get_tick(self):
        return self.tick_counter

    def add_target(self, x, y):
        visiting_particles = random.sample(self.particles, DEFAULT_VISITING_COUNT)
        t = Target(x,y, visiting_particles)
        self.targets.append(t)



    def destroy_targets(self):
        for target in self.targets:
            target.destroy()
        self.targets = []


