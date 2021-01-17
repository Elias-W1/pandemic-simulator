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
        self.simulation = None
        default_particle_count = 80

        # create view and simulation
        self.ui = View()


        # set standard values
        self.ui.countInput.setText(str(default_particle_count))
        self.ui.infectedInput.setText("1")
        self.ui.fpsInput.setText(str(fps))
        self.ui.speedInput.setText(str(speed))

        # connect signals
        self.ui.play_pause_simulation_signal.connect(self.play_pause_simulation)
        self.ui.reset_simulation_signal.connect(self.reset_simulation)
        self.ui.export_data_signal.connect(self.export)
        self.ui.granularity_changed_signal.connect(self.refresh_granularity)

        # simulation not active at start.
        self.active = False

        # set initial granularity
        self.granularity = self.refresh_granularity()

        # init statistic
        self.dead_count_history = []
        self.infected_count_history = []
        self.recovered_count_history = []
        self.healthy_count_history = []

        # Initialize graph values.
        self.infected_history = [0]
        self.healthy_history = [self.ui.get_particle_count()]
        self.recovered_history = [0]
        self.dead_history = [0]
        self.frame_history = [0]


        self.framecounter = 0

        # init graph plots
        self.infected_plot = self.ui.create_infected_plot(self.frame_history, self.infected_history)
        self.healthy_plot = self.ui.create_healthy_plot(self.frame_history, self.healthy_history)
        self.dead_plot = self.ui.create_dead_plot(self.frame_history, self.dead_history)
        self.recovered_plot = self.ui.create_recovered_plot(self.frame_history, self.recovered_history)



    def init_simulation(self):
        self.simulation = Simulation()
        # set particle size in view and simulation
        self.ui.set_particle_size(self.particle_size)
        self.simulation.set_particle_size(self.particle_size)
        particle_count = self.ui.get_particle_count()
        infected_count = self.ui.get_infected_count()
        self.simulation.death_rate =  int(self.ui.deathRateInput.text()) / 100
        self.simulation.infection_time = int(self.ui.infectionTimeInput.text())
        self.simulation.recovered_time = int(self.ui.recoveredTimeInput.text())

        self.simulation.create_particles(particle_count, infected_count)


        # create timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.mainloop)
        self.timer.start(1000 // fps)


    def play_pause_simulation(self):
        if self.active == False:
            self.play_simulation()
        else:
            self.pause_simulation()

    def pause_simulation(self):
        self.ui.startBtn.setText("Play")
        self.active = False

    def play_simulation(self):
        self.ui.startBtn.setText("Pause")
        if self.simulation == None:
            self.init_simulation()
        self.active = True

    def reset_simulation(self): # rough reset method.
        self.timer.stop()
        self.simulation = None
        self.init_simulation()
        self.ui.reset_scene()

        # reset statistics
        self.dead_count_history = []
        self.healthy_count_history = []
        self.recovered_count_history = []
        self.infected_history = []


        # reset graph values.
        self.infected_plot.clear()
        self.healthy_plot.clear()
        self.recovered_plot.clear()
        self.dead_plot.clear()
        self.infected_history = [0]
        self.frame_history = [0]
        self.framecounter = 0
        self.healthy_history = [self.ui.get_particle_count()]
        self.recovered_history = [0]
        self.dead_history = [0]
        self.frame_history = [0]

        self.pause_simulation()




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

            if self.framecounter % fps//2 == 0 and self.check_graph_value_changed():
                self.frame_history.append(self.framecounter)
                self.infected_history.append(self.simulation.infected_count / self.simulation.particle_count)
                self.healthy_history.append((self.simulation.particle_count - self.simulation.infected_count) / self.simulation.particle_count)
                self.recovered_history.append(self.simulation.recovered_count / self.simulation.particle_count)
                self.dead_history.append(self.simulation.dead_count / self.simulation.particle_count)
                self.set_graph()

    def check_graph_value_changed(self):
        changed = False
        if self.infected_history[-1] != (self.simulation.infected_count / self.simulation.particle_count):
            changed = True
        elif self.healthy_history[-1] != ((self.simulation.particle_count - self.simulation.infected_count) / self.simulation.particle_count):
            changed = True
        elif self.recovered_history[-1] != (self.simulation.recovered_count / self.simulation.particle_count):
            changed = True
        elif  self.dead_history[-1] != (self.simulation.dead_count / self.simulation.particle_count):
            changed = True

        return changed

    def set_graph(self):
        self.infected_plot.setData(self.frame_history, self.infected_history)
        self.healthy_plot.setData(self.frame_history, self.healthy_history)
        self.recovered_plot.setData(self.frame_history, self.recovered_history)
        self.dead_plot.setData(self.frame_history, self.dead_history)

    def export(self):
        healthy_count_history_granular = self.adapt_list_to_granularity(self.healthy_count_history)
        infected_count_history_granular = self.adapt_list_to_granularity(self.infected_count_history)
        recovered_count_history_granular = self.adapt_list_to_granularity(self.recovered_count_history)
        dead_count_history_granular = self.adapt_list_to_granularity(self.dead_count_history)
        granularity_steps = self.create_granularity_step_list(len(healthy_count_history_granular))


        df = pd.DataFrame(list(zip(healthy_count_history_granular, infected_count_history_granular, recovered_count_history_granular, dead_count_history_granular)), index=granularity_steps, columns=["Gesund", "Infiziert","Erholt","Tot"])
        df.index.name = "Zeitschritt"
        # df.to_csv(r"C:\Users\Elias\Desktop\out.csv")
        export_path = self.ui.choose_export_file()[0]
        if export_path == "":
            pass
        else:
            try:
                df.to_csv(export_path)
            except Exception as e:
                print("Exception occured when exporting file.\n",str(e),"\n\n")

    def adapt_list_to_granularity(self, listobj):
        newlist = []
        index = 0
        while index <= len(listobj)-1:
            newlist.append(listobj[index])
            index += self.granularity

        print("Len:" ,len(newlist), " | List: ",str(newlist))
        return newlist

    def create_granularity_step_list(self, length):
        listobj = []
        for i in range(length):
            listobj.append(i*self.granularity)
        print("Len:" ,len(listobj), " | List: ",str(listobj))
        return listobj

    def refresh_granularity(self):
        self.granularity = self.ui.granularitySlider.value()
        self.ui.granularityLabel.setText(str(self.granularity))