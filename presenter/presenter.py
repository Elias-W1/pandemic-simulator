from view.view import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QApplication
from model.simulation import Simulation


class Presenter(QtCore.QObject):
    def __init__(self):
        super(Presenter, self).__init__()
        self.particle_size = 10
        self.simulation = None

        # create view and simulation
        self.ui = View()

        # connect signals
        self.connect_signals()

        # simulation not active at start.
        self.active = False

        self.fps = 60
        self.speed = 1

        # OLD | DELETE LATER:::::::::::::

        # # Initialize graph values.
        # self.infected_history = [0]
        # self.healthy_history = [int(self.ui.countInput.text())]
        # self.recovered_history = [0]
        # self.dead_history = [0]
        # self.frame_history = [0]
        # # init statistic
        # self.dead_count_history = []
        # self.infected_count_history = []
        # self.recovered_count_history = []
        # self.healthy_count_history = []
        # self.init_graph_plots2()



    def connect_signals(self):
        self.ui.play_pause_simulation_signal.connect(self.play_pause_simulation)
        self.ui.reset_simulation_signal.connect(self.reset_simulation)
        self.ui.export_data_signal.connect(self.start_export)

    def init_graph_plots(self):
        data = self.simulation.statistics.get_live_data()
        self.ui.init_plotting_data(data[1],data[2])


    def init_simulation(self):
        self.simulation = Simulation(*self.ui.get_simulation_parameters(), particle_size=self.particle_size)
        self.ui.set_particle_size(self.particle_size)
        self.init_graph_plots()
        self.create_simulation_timer()
        self.create_fps_timer()

    def create_fps_timer(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.gui_mainloop)
        self.timer.start(1000 // self.fps)

    def create_simulation_timer(self):
        self.sim_timer = QtCore.QTimer(self)
        self.sim_timer.timeout.connect(self.simulation_mainloop)
        self.sim_timer.start(1000 // (100*self.fps))

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

    def reset_simulation(self):
        self.timer.stop()
        self.sim_timer.stop()
        self.simulation = None
        self.init_simulation()
        self.ui.reset_scene()
        self.ui.reset_plots()
        self.pause_simulation()


    def simulation_mainloop(self):
        if self.active:
            self.simulation.tick()

    def gui_mainloop(self):
        if self.active:
            self.ui.draw_particles(self.simulation.particles)
            self.ui.update_status_labels(*self.simulation.get_status_counts())
            if self.simulation.statistics.check_graph_value_changed() or self.simulation.tick_counter % self.fps // 2 == 0:
                self.ui.update_graph(*self.simulation.statistics.get_live_data())
                # self.update_statistics()


    def start_export(self):
        if self.simulation != None:
            self.ui.export(*self.simulation.statistics.get_export_data(self.ui.get_granularity()))
        else:
            print("No data to export yet. Start Simulation to get data.")


    #OLD GRAPH METHODS DELTE LATER:
    # def set_graph(self):
    #     self.infected_plot.setData(self.frame_history, self.infected_history)
    #     self.healthy_plot.setData(self.frame_history, self.healthy_history)
    #     self.recovered_plot.setData(self.frame_history, self.recovered_history)
    #     self.dead_plot.setData(self.frame_history, self.dead_history)
    #
    # def update_statistics(self):
    #     self.dead_count_history.append(self.simulation.dead_count)
    #     self.recovered_count_history.append(self.simulation.recovered_count)
    #     self.infected_count_history.append(self.simulation.infected_count)
    #     self.healthy_count_history.append(self.simulation.healthy_count)
    #
    #     if self.simulation.tick_counter % self.fps // 2 == 0:
    #         self.frame_history.append(self.simulation.tick_counter)
    #         self.infected_history.append(self.simulation.infected_count / self.simulation.particle_count)
    #         self.healthy_history.append(
    #             (self.simulation.particle_count - self.simulation.infected_count) / self.simulation.particle_count)
    #         self.recovered_history.append(self.simulation.recovered_count / self.simulation.particle_count)
    #         self.dead_history.append(self.simulation.dead_count / self.simulation.particle_count)
    #         self.set_graph()
    #
    # def reset_graph_values(self):
    #     # reset graph values.
    #     self.infected_plot.clear()
    #     self.healthy_plot.clear()
    #     self.recovered_plot.clear()
    #     self.dead_plot.clear()
    #     self.infected_history = [0]
    #     self.frame_history = [0]
    #     self.framecounter = 0
    #     self.healthy_history = [int(self.ui.countInput.text())]
    #     self.recovered_history = [0]
    #     self.dead_history = [0]
    #     self.frame_history = [0]
    #
    # def init_graph_plots2(self):
    #     self.infected_plot = self.ui.create_infected_plot(self.frame_history, self.infected_history)
    #     self.healthy_plot = self.ui.create_healthy_plot(self.frame_history, self.healthy_history)
    #     self.dead_plot = self.ui.create_dead_plot(self.frame_history, self.dead_history)
    #     self.recovered_plot = self.ui.create_recovered_plot(self.frame_history, self.recovered_history)
    #
