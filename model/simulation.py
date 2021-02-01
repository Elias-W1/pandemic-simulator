import random
from model.particle import *
from model.Statistics import *

def get_reversed(listobj):
    newlist = list(listobj).copy()
    newlist.reverse()
    return newlist



class Simulation():
    def __init__(self, particle_count, infected_count, death_rate, infection_time, recovery_time, particle_size):
        self.infected_count = infected_count
        self.particle_count = particle_count
        self.healthy_count = particle_count - infected_count
        self.dead_count = 0
        self.recovered_count = 0

        self.particle_size = particle_size
        self.death_rate = death_rate
        self.infection_time = infection_time
        self.recovery_time = recovery_time
        self.infection_radius = 3

        self.x_border = 600
        self.y_border = 600
        self.particles = []
        self.tick_counter = 0

        self.statistics = Statistics(self.particle_count, self.infected_count)
        self.create_particles()


    def create_particles(self):
        abssize = self.particle_size*2+1
        particles_per_row = (self.x_border // abssize) // 2
        rows_maximum = (self.y_border // abssize) // 2
        rows = self.particle_count // particles_per_row
        print("DEBUG PRINT: Maximum: ", particles_per_row*rows_maximum)
        if self.particle_count % particles_per_row > 0:
            rows = rows + 1

        print("DEBUG PRINT: ",rows,"<", rows_maximum,"?")

        assert rows < rows_maximum, "Rows maximum exceeded." # this is not good. todo


        print("Particles per row: ",particles_per_row)
        print("rows maximum: ",rows_maximum)

        # Make randomly scrambled list with infected/healthy status strings to randomize positions of infected and healthy particles later.
        particles = ["i"]*self.infected_count
        particles.extend(["h"]*(self.particle_count-self.infected_count))
        random.shuffle(particles)

        for i in range(len(particles)):
            status = particles[i]
            x = ((i+1) % particles_per_row)+1
            y = ((i+1) // rows_maximum) + 1
            print("i: ",i,"x:",x,"y:",y)

            self.create_particle(status, abssize * x * 2 , self.y_border - (abssize * y * 2)  )

    def set_infected_count(self, newcount):
        self.infected_count = newcount

    def create_particle(self, status, startx, starty):
        moving_dirs = [-1,1]
        particle = Particle(status, startx, starty, random.choice(moving_dirs), random.choice(moving_dirs), self.death_rate, self.infection_time, self.recovery_time, self.infection_radius)
        if status == "i":
            particle.set_status_infected(self.tick_counter)
        self.particles.append(particle)

    def particle_routine(self):
        collided_particles = []
        for particle in self.particles:
            # check for particle collisions and adjust movement
            for particle_b in self.particles:
                pair = [particle, particle_b]
                if particle == particle_b or get_reversed(pair) in collided_particles or (particle.status == "d" or particle_b.status == "d"):
                    continue

                collision, new_infections = particle.collides_with(particle_b, self.tick_counter)
                self.infected_count += new_infections
                if collision:
                    collided_particles.append(pair)

            # check for wall collisions and adjust movement accordingly
            particle.adjust_movement_wallcollision(self.x_border, self.y_border)
            particle.move()

            # update status of particle and counts of each status in simulation
            dead, recovered, healthy = particle.update_status(self.tick_counter)
            self.dead_count += dead
            self.recovered_count += recovered
            self.infected_count -= (dead+recovered)
            self.recovered_count -= healthy


    def set_measures(self, social_distancing=False):
        self.social_distancing = social_distancing

    def tick(self):
        self.particle_routine()
        self.tick_counter += 1
        self.healthy_count = self.particle_count - self.infected_count - self.dead_count - self.recovered_count
        self.statistics.add_data(self.healthy_count, self.infected_count, self.recovered_count, self.dead_count)

    def get_status_counts(self):
        return self.healthy_count, self.infected_count, self.recovered_count, self.dead_count
