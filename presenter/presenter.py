from view.view import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QApplication
from model.simulation import Simulation
import time

fps = 60

#TODO: implement graph

class Presenter(QtCore.QObject):
    def __init__(self):
        super(Presenter, self).__init__()

        self.particle_size = 10

        # Initialize graph values.
        self.infected_history = [0]
        self.frame_history = [0]
        self.framecounter = 0

        # create view and simulation
        self.ui = View()
        self.simulation = Simulation()

        # set particle size in view and simulation
        self.ui.set_particle_size(self.particle_size)
        self.simulation.set_particle_size(self.particle_size)

        # set standard values
        self.ui.countInput.setText("80")
        self.ui.infectedInput.setText("1")

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

    def start_stop_simulatiuon(self):   #TODO: implement start/stop button and reset button.
        pass

    def set_graph(self):
        self.ui.graph.plot(self.frame_history, self.infected_history)

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

            if self.framecounter % 10 == 0:
                self.frame_history.append(self.framecounter)
                self.infected_history.append(self.simulation.infected_count / self.simulation.particle_count)
                self.set_graph()