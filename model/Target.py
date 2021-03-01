from model.Constants import *

class Target():
    def __init__(self, x, y, waiting_duration=DEFAULT_TARGET_WAITING_DURATION, visiting_count=DEFAULT_VISITING_COUNT):
        self.x = x
        self.y = y
        self.waiting_duration = DEFAULT_TARGET_WAITING_DURATION # in ticks
        self.visiting_count = DEFAULT_VISITING_COUNT
        self.visiting_particles = []

    def destroy(self):
        for particle in self.visiting_particles:
            particle.remove_target()

    def add_visitor(self, particle):
        self.visiting_particles.append(particle)

    def reached(self, particle):
        pass
