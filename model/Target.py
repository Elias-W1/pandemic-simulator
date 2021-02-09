from model.Constants import *

class Target():
    def __init__(self, x, y, visiting_particles):
        self.x = x
        self.y = y
        self.waiting_duration = DEFAULT_TARGET_WAITING_DURATION # in ticks
        self.visiting_count = DEFAULT_VISITING_COUNT
        self.no_visit_duration = DEFAULT_NO_VISIT_DURATION

        self.visiting_particles = visiting_particles
        self.set_visitors_target()

    def destroy(self):
        for particle in self.visiting_particles:
            particle.target = None

    def set_visitors_target(self):
        for particle in self.visiting_particles:
            particle.target = self
            particle.movement = Movement.DIRECTED
            particle.x_movement = particle.stepsize_multiplier
            particle.y_movement = particle.stepsize_multiplier
