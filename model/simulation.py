import math
from random import randint
import random
import time

def get_reversed(listobj):
    newlist = listobj.copy()
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
        self.set_infected_count(0)

    def create_particles(self, count, count_infected):      # TODO: MAKE PARTICLES SPAWN NOT OVERLAPPING
        self.particle_count = count
        self.particles = []
        for i in range(count_infected):
            self.create_particle("i")

        for i in range(count - count_infected):
            self.create_particle("h")

        self.set_infected_count(count_infected)

    def set_particle_size(self, particle_size):
        self.particle_size = particle_size

    def set_infected_count(self, newcount):
        if self.infected_count != newcount:
            print("{count} particles infected.".format(count=newcount))
        self.infected_count = newcount

    def create_particle(self, status):
        moving_dirs = [-1,1]
        self.particles.append(Particle(status, randint(0, self.x_border-(self.particle_size*2+1)), randint(0, self.y_border-(self.particle_size*2+1)), random.choice(moving_dirs), random.choice(moving_dirs)))

    def move_particles(self):
        """Move particles"""
        #TODO: MAKE CORRECT WALL COLLISION CHECK.
        for particle in self.particles:
            if particle.x-particle.size//2+particle.x_movement-1 <= 0 or particle.x+particle.size//2+particle.x_movement+1 >= self.x_border:
                particle.repel_x()
            particle.x = particle.x + particle.x_movement

            if particle.y-particle.size//2+particle.y_movement-1 <= 0 or particle.y+particle.size//2+particle.y_movement+1 >= self.y_border:
                particle.repel_y()
            particle.y = particle.y + particle.y_movement



    def tick(self):
        self.check_collision()
        self.move_particles()
        # print("({x},{y})".format(x=self.particles[0].x,y=self.particles[0].y)) # see if first particle moved for debugging.

        # update infected counter.
        infected_count = 0
        for p in self.particles:
            if p.status == "i":
                infected_count = infected_count + 1
        self.set_infected_count(infected_count)


    def check_collision(self):
        """Checks if any particles of the simulation collide with each other, starts collision routine."""

        # get collision pairs to prevent double collision in loop
        collision_pairs = []

        hitbox_size = self.particle_size*2+1
        # assuming square hitbox.
        for a in range(len(self.particles)):
            particle_a = self.particles[a]
            hitbox_a_x = particle_a.x
            for b in range(len(self.particles)):
                particle_b = self.particles[b]

                pair = [(particle_a.x, particle_a.y), (particle_b.x, particle_b.y)]
                if particle_a == particle_b:   # if particle_a == particle_b or collision already resolved for those particles: continue
                    continue
                elif get_reversed(pair) in collision_pairs:
                    continue

                # Check for collision of the 2 hitboxes.
                if self.check_particle_intersection(particle_a, particle_b):
                    # print("Collision of particle " + str(a) + " and particle " + str(b))
                    self.collide(particle_a, particle_b)
                    collision_pairs.append(pair)

    def check_particle_intersection(self, particle_a, particle_b):
        return check_intersection(particle_a.x-self.particle_size//2, particle_a.y-self.particle_size//2, particle_a.x+self.particle_size//2, particle_a.y+self.particle_size//2, particle_b.x-self.particle_size//2, particle_b.y-self.particle_size//2, particle_b.x+self.particle_size//2, particle_b.y+self.particle_size//2)
        # return check_intersection(particle_a.x-self.particle_size, particle_a.y-self.particle_size, particle_a.x+self.particle_size, particle_a.y+self.particle_size, particle_b.x-self.particle_size, particle_b.y-self.particle_size, particle_b.x+self.particle_size, particle_b.y+self.particle_size)

    def collide(self, particle_a, particle_b):
        """Collision of 2 particles routine."""
        # print("Collision at ({x1},{y1}) and ({x2},{y2})".format(x1=particle_a.x,x2=particle_b.x, y1=particle_a.y, y2=particle_b.y))
        if particle_a.status == "i" and particle_b.status == "h":
            print("A infects B.")
            particle_b.change_status("i")
        elif particle_a.status == "h" and particle_b.status == "i":
            particle_a.change_status("i")
            print("B infects A.")

        # particles repelling
        #TODO: find right repelling.
        particle_a.repel_x()
        particle_a.repel_y()
        particle_b.x_movement = particle_a.x_movement * (-1)
        particle_b.y_movement = particle_a.y_movement * (-1)


    def set_measures(self, social_distancing=False):
        #todo: implement measures.
        self.social_distancing = social_distancing


class Particle():
    def __init__(self, status, x, y, x_movement, y_movement):
        print("Initializing {status} particle at {x},{y}".format(status=status,x=x,y=y))
        self.status = status    # status can be h(ealthy), i(nfected), d(ead) or r(ecovered).
        self.x = x
        self.y = y
        self.x_movement = x_movement       # movement on X. negative = left and positive = right. Absolute value = speed.
        self.y_movement = y_movement
        self.size = 2           # size = radius.

    def change_status(self, newstatus):
        self.status = newstatus

    def repel_x(self):
        self.x_movement = self.x_movement * (-1)

    def repel_y(self):
        self.y_movement = self.y_movement * (-1)





if __name__ == "__main__":
    print("Debugging Simulation")
    s = Simulation()
    s.create_particles(50, 15)
    fps = 60
    while True:
        s.tick()
        time.sleep(1/fps)


