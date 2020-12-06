from view.view import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QApplication
from model.simulation import Simulation
import time

fps = 60

class Presenter(QtCore.QObject):
    def __init__(self):
        super(Presenter, self).__init__()

        self.particle_size = 20

        # create view and simulation
        self.ui = View()
        self.simulation = Simulation()

        # set particle size in view and simulation
        self.ui.set_particle_size(self.particle_size)
        self.simulation.set_particle_size(self.particle_size)

        # connect signals
        self.ui.start_simulation_signal.connect(self.start_simulation)


    def start_simulation(self):
        # TODO: Make robust:
        particle_count = int(self.ui.countInput.text())
        infected_count = int(self.ui.infectedInput.text())
        self.simulation.create_particles(particle_count, infected_count)

        # create timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.mainloop)
        self.timer.start(1000 // fps)
        self.framecounter = 0

    def mainloop(self):
            self.simulation.tick()
            self.ui.reset_scene()
            particles = self.simulation.particles
            for particle in particles:
                self.ui.draw_particle(particle.x, particle.y, particle.status)
            self.ui.set_scene()
            self.framecounter += 1
            self.ui.set_infectedLabel(self.simulation.infected_count)
            self.ui.set_healthyLabel(self.simulation.particle_count - self.simulation.infected_count)