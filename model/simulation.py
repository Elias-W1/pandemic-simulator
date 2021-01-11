import itertools
import math
from random import randint
import random


def get_reversed(listobj):
    newlist = list(listobj).copy()
    newlist.reverse()
    return newlist

def check_intersection(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2): # https://silentmatt.com/rectangle-intersection/
    if (ax1 < bx2) and (ax2 > bx1) and (ay1 < by2) and (ay2 > by1):
        return True
    else:
        return False

class Simulation():
    def __init__(self):
        self.x_border = 600
        self.y_border = 600
        self.infected_count = 0
        self.particle_count = 0
        self.dead_count = 0
        self.recovered_count = 0
        self.set_infected_count(0)

        self.death_rate = 0.03
        self.infection_time = 336       # 7 * 24 * 2 ticks
        self.recovery_time = 600        # arbitrary

        self.tick_counter = 0


    def create_particles(self, count, count_infected):

        self.particle_count = count
        self.particles = []

        self.abssize = self.particle_size * 2 + 1

        particles_per_row = (self.x_border // self.abssize) // 2
        rows_maximum = (self.y_border // self.abssize) // 2
        rows = count // particles_per_row
        print("Maximum: ", particles_per_row*rows_maximum)
        if count % particles_per_row > 0:
            rows = rows + 1

        print(rows,"<", rows_maximum)

        assert rows < rows_maximum, "Rows maximum exceeded."


        print("Particles per row: ",particles_per_row)
        print("rows maximum: ",rows_maximum)

        # Make randomly scrambled list with infected/healthy status strings to randomize positions of infected and healthy particles later.
        particles = ["i"]*count_infected
        particles.extend(["h"]*(count-count_infected))
        random.shuffle(particles)

        for i in range(len(particles)):
            status = particles[i]
            x = ((i+1) % particles_per_row)+1
            y = ((i+1) // rows_maximum) + 1
            print("i: ",i,"x:",x,"y:",y)

            self.create_particle(status, self.abssize * x * 2 , self.y_border - (self.abssize * y * 2)  )

        # for i in range(count_infected):
        #     self.create_particle("i", randint(0, self.x_border - (self.particle_size * 2 + 1)), randint(0, self.y_border - (self.particle_size * 2 + 1)))
        #
        # for i in range(count - count_infected):
        #     self.create_particle("h", randint(0, self.x_border - (self.particle_size * 2 + 1)), randint(0, self.y_border - (self.particle_size * 2 + 1)))

        self.set_infected_count(count_infected)

    def set_particle_size(self, particle_size):
        self.particle_size = particle_size

    def set_infected_count(self, newcount):
        self.infected_count = newcount


    def create_particle(self, status, startx, starty):
        moving_dirs = [-1,1]
        particle = Particle(status, startx, starty, random.choice(moving_dirs), random.choice(moving_dirs))
        if status == "i":
            particle.set_status_infected(self.tick_counter)
        self.particles.append(particle)

    def particle_routine(self):
        """Routine for particles. Move particles, update infected count, recovery/death"""

        for particle in self.particles:
            if particle.x-(particle.size+1)+particle.x_movement-1 <= 0 and particle.x_movement < 0:
                particle.repel_x()
            elif particle.x+self.abssize*2+particle.x_movement+1 >= self.x_border-self.particle_size and particle.x_movement > 0:
                particle.repel_x()

            if particle.y-(particle.size+1)+particle.y_movement-1 <= 0 and particle.y_movement < 0:
                particle.repel_y()
            elif particle.y+(particle.size+1)+particle.y_movement+1 >= self.y_border-self.particle_size and particle.y_movement > 0:
                particle.repel_y()

            particle.move()

            if (particle.infection_start_tick > -1) and (self.tick_counter - particle.infection_start_tick >= self.infection_time):
                particle.end_infection(self.tick_counter, self.death_rate)
                self.infected_count -= 1
                if particle.status == "d":
                    self.dead_count += 1
                else:
                    self.recovered_count += 1


            if particle.recovery_start_tick > -1 and (self.tick_counter - particle.recovery_start_tick >= self.recovery_time):
                particle.change_status("h")
                particle.recovery_start_tick = -1
                self.recovered_count -= 1



    def check_collision(self):
        """Checks if any particles of the simulation collide with each other, starts collision routine."""
        collision_pairs = []
        combinations = itertools.product(self.particles, self.particles)
        for c in combinations:
            particle_a = c[0]
            particle_b = c[1]
            if particle_a == particle_b or (get_reversed(c) in collision_pairs) or particle_a.status == "d" or particle_b.status == "d":
                continue
            if self.check_particle_intersection(particle_a, particle_b):
                self.collide(particle_a, particle_b)
                collision_pairs.append(c)

    def check_particle_intersection(self, particle_a, particle_b):
        return check_intersection(particle_a.x-self.particle_size//2, particle_a.y-self.particle_size//2, particle_a.x+self.particle_size//2, particle_a.y+self.particle_size//2, particle_b.x-self.particle_size//2, particle_b.y-self.particle_size//2, particle_b.x+self.particle_size//2, particle_b.y+self.particle_size//2)


    def collide(self, particle_a, particle_b):
        """Collision of 2 particles routine."""
        # print("Collision at ({x1},{y1}) and ({x2},{y2})".format(x1=particle_a.x,x2=particle_b.x, y1=particle_a.y, y2=particle_b.y)) debug message
        if particle_a.status == "i" and particle_b.status == "h":
            particle_b.set_status_infected(self.tick_counter)
            self.infected_count += 1
        elif particle_a.status == "h" and particle_b.status == "i":
            particle_a.set_status_infected(self.tick_counter)
            self.infected_count += 1

        # particles repelling
        particle_a.repel_x()
        particle_a.repel_y()
        particle_b.x_movement = particle_a.x_movement * (-1)
        particle_b.y_movement = particle_a.y_movement * (-1)

        particle_a.move()
        particle_b.move()


    def set_measures(self, social_distancing=False):
        #todo: implement measures.
        self.social_distancing = social_distancing

    def tick(self):
        self.check_collision()
        self.particle_routine()
        # print("({x},{y})".format(x=self.particles[0].x,y=self.particles[0].y)) # see if first particle moved for debugging.

        self.tick_counter += 1


class Particle():
    def __init__(self, status, x, y, x_movement, y_movement):
        print("Initializing {status} particle at {x},{y}".format(status=status,x=x,y=y))
        self.status = status               # status can be h(ealthy), i(nfected), d(ead) or r(ecovered).
        self.x = x
        self.y = y
        self.x_movement = x_movement       # movement on X. negative = left and positive = right. Absolute value = speed.
        self.y_movement = y_movement
        self.size = 2           # size = radius.
        self.infection_start_tick = -1
        self.recovery_start_tick = -1

    def change_status(self, newstatus):
        self.status = newstatus

    def set_status_infected(self, current_tick):
        self.status = "i"
        self.infection_start_tick = current_tick

    def repel_x(self):
        self.x_movement = self.x_movement * (-1)

    def repel_y(self):
        self.y_movement = self.y_movement * (-1)

    def move(self):
        self.x = self.x + self.x_movement
        self.y = self.y + self.y_movement

    def end_infection(self, current_tick, death_rate):
        random = randint(1,100)
        if random/100 <= death_rate:      # die
            self.change_status("d")
            self.x_movement = 0
            self.y_movement = 0
            print("particle died")
        else:                               # recover
            self.change_status("r")
            self.recovery_start_tick = current_tick
        self.infection_start_tick = -1









if __name__ == "__main__":
    print("Debugging Simulation")
    a = []
    for p in range(5): a.append("Particle"+str(p))
    print(a)


    # fps = 60
    # while True:
    #     s.tick()
    #     time.sleep(1/fps)


