import math
from random import randint
import random
import time

class Simulation():
    def __init__(self, particle_size):
        self.particle_size = 2  # TODO: GIVE PARTICLE SIZE TO PARTICLES
        self.x_border = 600
        self.y_border = 600

        self.set_infected_count(0)

    def create_particles(self, count, count_infected):
        self.particles = []
        for i in range(count_infected):
            self.create_particle("i")

        for i in range(count - count_infected):
            self.create_particle("h")

        self.set_infected_count(count_infected)

    def set_infected_count(self, newcount):
        self.infected_count = newcount
        print("{count} particles infected.".format(count=self.infected_count))

    def create_particle(self, status):
        moving_dirs = [-1,1]
        self.particles.append(Particle(status, randint(0, self.x_border-(self.particle_size*2+1)), randint(0, self.y_border-(self.particle_size*2+1)), random.choice(moving_dirs), random.choice(moving_dirs)))

    def move_particles(self):
        """Move particles"""
        #TODO: MAKE REAL WALL COLLISION CHECK.
        for particle in self.particles:
            if particle.x+particle.x_movement < 0 or particle.x+particle.x_movement > self.x_border:
                particle.repel_x()
            particle.x = particle.x + particle.x_movement

            if particle.y+particle.y_movement < 0 or particle.y+particle.y_movement > self.y_border:
                particle.repel_y()
            particle.y = particle.y + particle.y_movement

    def tick(self):
        self.move_particles()
        self.check_collision()
        # print("({x},{y})".format(x=self.particles[0].x,y=self.particles[0].y)) # see if first particle moved for debugging.

        # update infected counter.
        infected_count = 0
        for p in self.particles:
            if p.status == "i":
                infected_count = infected_count + 1
        self.set_infected_count(infected_count)


    def check_collision(self):  #TODO: Remove double collision check on a single collision
        """Checks if any particles of the simulation collide with each other, starts collision routine."""
        hitbox_size = self.particle_size*2+1
        # assuming square hitbox.
        for a in range(len(self.particles)):
            particle_a = self.particles[a]
            hitbox_a_x = particle_a.x
            for b in range(len(self.particles)):
                particle_b = self.particles[b]
                if particle_a == particle_b:
                    continue

                # Check for collision of the 2 hitboxes.
                # https://gamedev.stackexchange.com/questions/586/what-is-the-fastest-way-to-work-out-2d-bounding-box-intersection
                if (abs(particle_a.x - particle_b.x) * 2 < hitbox_size*2 and (abs(particle_a.y - particle_b.y) * 2 < hitbox_size*2)):
                    self.collide(particle_a, particle_b)




    def collide(self, particle_a, particle_b):
        """Collision of 2 particles routine."""
        print("Collision")
        if particle_a.status == "i" and particle_b.status == "h":
            print("A infects B.")
            particle_b.change_status("i")
        elif particle_a.status == "h" and particle_b.status == "i":
            particle_a.change_status("i")
            print("B infects A.")
        else:
            print("No new infection")

        # particles repelling
        particle_b.repel_x()
        particle_b.repel_y()


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


