from view.view import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QApplication
from model.simulation import Simulation
import pandas as pd

fps = 60
speed = 1


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

        # set standard values
        self.ui.countInput.setText("80")
        self.ui.infectedInput.setText("1")
        self.ui.fpsInput.setText(str(fps))
        self.ui.speedInput.setText(str(speed))

        # connect signals
        self.ui.play_pause_simulation_signal.connect(self.play_pause_simulatiuon)
        self.ui.reset_simulation_signal.connect(self.reset_simulation)
        self.ui.export_data_signal.connect(self.export)

        # init simulation
        self.active = False
        self.init_simulation()

        # init statistic
        self.dead_count_history = []
        self.infected_count_history = []
        self.recovered_count_history = []
        self.healthy_count_history = []

    def init_simulation(self):
        self.simulation = Simulation()
        # set particle size in view and simulation
        self.ui.set_particle_size(self.particle_size)
        self.simulation.set_particle_size(self.particle_size)
        # TODO: Make robust:
        particle_count = int(self.ui.countInput.text())
        infected_count = int(self.ui.infectedInput.text())
        self.simulation.death_rate =  int(self.ui.infectedInput.text()) / 100
        self.simulation.infection_time = int(self.ui.infectionTimeInput.text())
        self.simulation.recovered_time = int(self.ui.recoveredTimeInput.text())

        self.simulation.create_particles(particle_count, infected_count)


        # create timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.mainloop)
        self.timer.start(1000 // fps)


    def play_pause_simulatiuon(self):
        if self.active == False:
            self.ui.startBtn.setText("Pause")
        else:
            self.ui.startBtn.setText("Play")

        self.active = not self.active

    def reset_simulation(self): # rough reset method.
        self.timer.stop()
        self.simulation = None
        self.init_simulation()

        # reset statistics
        self.dead_count_history = []
        self.healthy_count_history = []
        self.recovered_count_history = []
        self.infected_history = []

        # reset graph
        self.ui.reset_graph()

        # reset graph values.
        self.infected_history = [0]
        self.frame_history = [0]
        self.framecounter = 0


    def set_graph(self):
        self.ui.graph.plot(self.frame_history, self.infected_history)

    def mainloop(self):
        if self.active:
            self.simulation.tick()
            self.ui.reset_scene()
            # draw particles
            particles = self.simulation.particles
            for particle in particles:
                self.ui.draw_particle(particle.x, particle.y, particle.status)
            self.ui.set_scene()

            self.framecounter += 1
            healthy_count = self.simulation.particle_count - self.simulation.infected_count - self.simulation.dead_count - self.simulation.recovered_count
            # update labels
            self.ui.set_infectedLabel(self.simulation.infected_count)
            self.ui.set_deadLabel(self.simulation.dead_count)
            self.ui.set_recoveredLabel(self.simulation.recovered_count)
            self.ui.set_healthyLabel(healthy_count)

            # update statistic
            self.dead_count_history.append(self.simulation.dead_count)
            self.recovered_count_history.append(self.simulation.recovered_count)
            self.infected_count_history.append(self.simulation.infected_count)
            self.healthy_count_history.append(healthy_count)


            if self.framecounter % fps == 0 and (self.simulation.infected_count / self.simulation.particle_count) != self.infected_history[-1]:
                self.frame_history.append(self.framecounter)
                self.infected_history.append(self.simulation.infected_count / self.simulation.particle_count)
                self.set_graph()

    def export(self):
        df = pd.DataFrame(list(zip(self.healthy_count_history, self.infected_count_history, self.recovered_count_history, self.dead_count_history)), index=list(range(len(self.healthy_count_history))), columns=["Gesund", "Infiziert","Erholt","Tot"])
        df.index.name = "Zeitschritt"
        df.to_csv(r"C:\Users\Elias\Desktop\out.csv")