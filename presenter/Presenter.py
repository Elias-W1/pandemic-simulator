from view.View import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QApplication
from model.Simulation import *
from presenter.Constants import *
from model.Constants import *

class Presenter(QtCore.QObject):
    def __init__(self):
        super(Presenter, self).__init__()
        self.particle_size = DEFAULT_PARTICLE_SIZE
        self.simulation = None
        self.ui = View()
        self.connect_signals()

        # simulation not active at start.
        self.active = False

        self.fps = DEFAULT_FPS
        self.speed = DEFAULT_SPEED

        self.init_timers()

    def connect_signals(self):
        self.ui.play_pause_simulation_signal.connect(self.play_pause_simulation)
        self.ui.reset_simulation_signal.connect(self.reset_simulation)
        self.ui.export_data_signal.connect(self.start_export)
        self.ui.fps_changed_signal.connect(self.update_fps)
        self.ui.speed_changed_signal.connect(self.update_speed)
        self.ui.stepsize_changed_signal.connect(self.update_stepsize)
        self.ui.movement_changed_signal.connect(self.update_movement_type)


    def init_graph_plots(self):
        data = self.simulation.statistics.get_live_data()
        self.ui.init_plotting_data(data[1],data[2])

    def init_timers(self):
        self.create_fps_timer()
        self.create_simulation_timer()

    def init_simulation(self):
        self.simulation = Simulation(*self.ui.get_simulation_parameters(), particle_size=self.particle_size)
        self.ui.set_particle_size(self.particle_size)
        self.init_graph_plots()
        self.update_stepsize()
        self.update_movement_type()
        self.simulation.set_measures(self.ui.get_measure_parameters())
        if self.timer == None:
            self.create_simulation_timer()
            self.create_fps_timer()

    def create_fps_timer(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.gui_mainloop)
        self.update_fps()
        self.timer.start(1000 // self.fps)

    def create_simulation_timer(self):
        self.sim_timer = QtCore.QTimer(self)
        self.sim_timer.timeout.connect(self.simulation_mainloop)
        self.update_speed()
        self.sim_timer.start(1000 // (60*self.speed))

    def update_speed(self):
        self.speed = self.ui.get_speed()
        if self.active:
            self.sim_timer.stop()
            self.sim_timer.start(1000 // (60*self.speed))

    def update_fps(self):
        print("Updating fps")
        newfps = self.ui.get_fps()
        if newfps > 0:
            self.fps = newfps
        print("new fps:",self.fps)
        if self.active:
            self.timer.stop()
            self.timer.start(1000 // self.fps)

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
        self.simulation = None
        self.ui.reset_simulation_routine()
        self.pause_simulation()

    def update_stepsize(self):
        if self.simulation != None:
            new_stepsize = self.ui.get_stepsize()
            was_active = self.active
            if was_active:
                self.pause_simulation()
            self.simulation.change_stepsize(new_stepsize)
            if was_active:
                self.play_simulation()

    def simulation_mainloop(self):
        if self.active:
            self.simulation.tick()

    def gui_mainloop(self):
        if self.active:
            self.ui.draw(self.simulation.particles, self.simulation.targets)
            self.ui.update_status_labels(*self.simulation.get_status_counts())
            if self.simulation.statistics.check_graph_value_changed() or self.simulation.tick_counter % self.fps // 2 == 0:
                self.ui.update_graph(*self.simulation.statistics.get_live_data())
                # self.update_statistics()

    def start_export(self):
        if self.simulation != None:
            self.ui.export(*self.simulation.statistics.get_export_data(self.ui.get_granularity()))
        else:
            print("No data to export yet. Start Simulation to get data.")

    def update_movement_type(self):
        if self.simulation != None:
            new_movement = self.ui.get_movement_type()
            self.simulation.set_movement(new_movement)
            if new_movement == Movement.DIRECTED:
                self.simulation.add_target(*self.ui.get_target_coordinates())
