from view.mainwindow import *
import pyqtgraph as pg
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QFileDialog
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtCore import Qt
import pandas as pd
from presenter.Constants import *
from view.Constants import *
from model.Constants import *

def check_intersection(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2): # https://silentmatt.com/rectangle-intersection/
    if (ax1 < bx2) and (ax2 > bx1) and (ay1 < by2) and (ay2 > by1):
        return True
    else:
        return False

class View(QtWidgets.QMainWindow, Ui_MainWindow):
    play_pause_simulation_signal = QtCore.pyqtSignal()   # signals do not work in the constructor apparently.
    reset_simulation_signal = QtCore.pyqtSignal()
    export_data_signal = QtCore.pyqtSignal()
    fps_changed_signal = QtCore.pyqtSignal()
    speed_changed_signal = QtCore.pyqtSignal()
    stepsize_changed_signal = QtCore.pyqtSignal()
    movement_changed_signal = QtCore.pyqtSignal()


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_widgets()
        self.connect_signals()

        self.create_colors()
        self.create_pens()
        self.create_brushes()
        self.set_default_values()

        self.graph.setYRange(0, 1)
        self.graph.setXRange(0,10000)




        self.last_drawn_tick = -1

    def init_stepsize_slider(self):
        self.stepsizeSlider.setMinimum(1)
        self.stepsizeSlider.setMaximum(5)


    def init_speed_slider(self):
        self.speedSlider.setMinimum(10)
        self.speedSlider.setMaximum(500)
        self.speedSlider.setValue(100)

    def create_colors(self):
        self.infected_color = QColor(255, 0, 0, 128)
        self.healthy_color = QColor(0, 255, 33, 255)
        self.dead_color = QColor(136, 136, 136, 128)
        self.recovered_color = QColor(12, 0, 193, 128)


    def set_particle_size(self, particle_size):
        self.particle_size = particle_size

    def create_pens(self):
        self.pen_infected = QPen(self.infected_color)
        self.pen_healthy = QPen(self.healthy_color)
        self.pen_dead = QPen(self.dead_color)
        self.pen_recovered = QPen(self.recovered_color)
        self.pen_masked = QPen(QColor(0, 208, 255, 255))

    def create_brushes(self):
        self.brush_infected = QBrush(self.infected_color, Qt.SolidPattern)
        self.brush_healthy = QBrush(self.healthy_color, Qt.SolidPattern)
        self.brush_dead = QBrush(self.dead_color, Qt.SolidPattern)
        self.brush_recovered = QBrush(self.recovered_color, Qt.SolidPattern)

    def create_widgets(self):
        """Initializes widgets."""
        # set 0,0 to bottom left.
        self.view.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.show()

        # create graph.
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('b')

        # Setting values for granularity slider.
        self.granularitySlider.setMinimum(1)
        self.granularitySlider.setMaximum(200)

        self.init_stepsize_slider()
        self.init_speed_slider()

    def set_default_values(self):
        self.countInput.setText(str(DEFAULT_PARTICLE_COUNT))
        self.infectedInput.setText(str(DEFAULT_INFECTED_COUNT))
        self.fpsInput.setText(str(DEFAULT_FPS))


    def draw_particle(self, particle):
        drawing_tools = self.select_drawing_tools(particle)
        self.scene.addEllipse(particle.x, particle.y, self.particle_size, self.particle_size, drawing_tools["pen"], drawing_tools["brush"])

    def select_drawing_tools(self, particle):
        status = particle.status
        if status == Status.HEALTHY:
            pen = self.pen_healthy
            brush = self.brush_healthy
        elif status == Status.INFECTED:
            pen = self.pen_infected
            brush = self.brush_infected
        elif status == Status.DEAD:
            pen = self.pen_dead
            brush = self.brush_dead
        elif status == Status.RECOVERED:
            pen = self.pen_recovered
            brush = self.brush_recovered
        else:
            print("Unrecognized status: "+status)
            pen = None
            brush = None

        if particle.masked:
            pen = self.pen_masked
        return {"pen": pen, "brush":brush}


    def reset_scene(self):
        self.scene.clear()

    def set_scene(self):
        self.view.setScene(self.scene)

    def reset_simulation_routine(self):
        self.reset_plots()
        self.reset_scene()
        self.reset_status_labels()
        self.last_drawn_tick = -1

    def get_measure_parameters(self):
        # Get mask parameters.
        masked = self.maskCb.isChecked()
        print(self.maskDd.currentText())
        if self.maskDd.currentText() == ABSOLUTE_VALUE_STRING:
            masked_count = self.int_from_input(self.maskInp, 0)
            masked_percentage = None
        elif self.maskDd.currentText() == PERCENTAGE_VALUE_STRING:
            masked_count = None
            masked_percentage = self.int_from_input(self.maskInp, 0)

        # Get social distancing parameters.
        social_distancing = self.socialDistancingCb.isChecked()
        if self.socialDistancingDd.currentText() == ABSOLUTE_VALUE_STRING:
            sd_count = self.int_from_input(self.socialDistancingInp, 0)
            sd_percentage = None
        elif self.socialDistancingDd.currentText() == PERCENTAGE_VALUE_STRING:
            sd_count = None
            sd_percentage = self.int_from_input(self.socialDistancingInp, 0)

        values = {"mask":masked, "masked_count":masked_count, "masked_percentage":masked_percentage,"social_distancing":social_distancing, "social_distancing_count":sd_count, "social_distancing_percentage":sd_percentage}

        return values


    def connect_signals(self):
        self.startBtn.pressed.connect(self.startBtn_clicked)
        self.resetBtn.pressed.connect(lambda: self.reset_simulation_signal.emit())
        self.exportBtn.pressed.connect(lambda: self.export_data_signal.emit())
        self.granularitySlider.valueChanged.connect(self.refresh_granularity)
        self.speedSlider.valueChanged.connect(lambda: self.speed_changed_signal.emit())
        self.fpsInput.textChanged.connect(lambda: self.fps_changed_signal.emit())
        self.stepsizeSlider.valueChanged.connect(lambda: self.stepsize_changed_signal.emit())
        self.diagonalRadio.toggled.connect(lambda: self.movement_changed_signal.emit())
        self.undirectedRadio.toggled.connect(lambda: self.movement_changed_signal.emit())
        self.directedRadio.toggled.connect(lambda: self.movement_changed_signal.emit())

    def startBtn_clicked(self):
        print("Start button pressed.")
        self.play_pause_simulation_signal.emit()

    def set_infectedLabel(self, count):
        self.infectedLabel.setText("{count} Erkrankt.".format(count=count))

    def set_healthyLabel(self, count):
        self.healthyLabel.setText("{count} Gesund.".format(count=count))

    def set_deadLabel(self, count):
        self.deadLabel.setText("{count} Gestorben.".format(count=count))

    def set_recoveredLabel(self, count):
        self.recoveredLabel.setText("{count} Genesen.".format(count=count))

    def choose_export_file(self):
        dlg = QFileDialog(caption='Save CSV File', directory="C:\\")
        dlg.setAcceptMode(QFileDialog.AcceptSave)
        return dlg.getSaveFileName(filter="CSV (*.csv)")

    def reset_status_labels(self):
        self.set_infectedLabel(0)
        self.set_healthyLabel(0)
        self.set_recoveredLabel(0)
        self.set_deadLabel(0)

    def init_plotting_data(self, healthy_count, infected_count):
        self.frame_history = [0]
        self.healthy_history = [healthy_count]
        self.infected_history = [infected_count]
        self.dead_history = [0]
        self.recovered_history = [0]
        self.init_graph_plots()

    def init_graph_plots(self):
        self.create_infected_plot(self.frame_history, self.infected_history)
        self.healthy_plot = self.create_healthy_plot(self.frame_history, self.healthy_history)
        self.create_dead_plot(self.frame_history, self.dead_history)
        self.recovered_plot = self.create_recovered_plot(self.frame_history, self.recovered_history)

    def create_infected_plot(self, x, y):
        self.infected_plot =  self.graph.plot(x, y, pen=[255,0,0,255])

    def create_healthy_plot(self, x, y):
        return self.graph.plot(x, y, pen=[0, 255, 33, 255])

    def create_recovered_plot(self, x, y):
        return self.graph.plot(x, y, pen=[12, 0, 193, 255])

    def create_dead_plot(self, x, y):
        self.dead_plot = self.graph.plot(x, y, pen=[136, 136, 136, 255])

    def reset_plots(self):
        self.infected_plot.clear()
        self.healthy_plot.clear()
        self.recovered_plot.clear()
        self.dead_plot.clear()
        self.frame_history = [0]
        self.healthy_history = [0]
        self.dead_history = [0]
        self.infected_history = [0]
        self.recovered_history =[0]

    def draw(self, particles, targets):
        self.reset_scene()
        self.draw_particles(particles)
        self.draw_targets(targets)
        self.set_scene()

    def draw_particles(self, particles):
        for particle in particles:
            self.draw_particle(particle)
            if particle.outlined:
                self.draw_outline(particle)


    def draw_outline(self,particle):
        drawing_tools = self.select_drawing_tools(particle)
        self.scene.addRect((particle.x-self.particle_size//2), (particle.y-self.particle_size//2), self.particle_size + particle.infection_abssize, self.particle_size + particle.infection_abssize, drawing_tools["pen"])

    def update_status_labels(self, healthy_count, infected_count, recovered_count, dead_count): # status label update und graph update zusammenfassen?
        self.set_infectedLabel(infected_count)
        self.set_deadLabel(dead_count)
        self.set_recoveredLabel(recovered_count)
        self.set_healthyLabel(healthy_count)

    def update_graph(self, new_frame, new_healthy, new_infected, new_recovered, new_dead):
        self.frame_history.append(new_frame)
        self.healthy_history.append(new_healthy)
        self.infected_history.append(new_infected)
        self.recovered_history.append(new_recovered)
        self.dead_history.append(new_dead)
        self.infected_plot.setData(self.frame_history, self.infected_history)
        self.healthy_plot.setData(self.frame_history, self.healthy_history)
        self.recovered_plot.setData(self.frame_history, self.recovered_history)
        self.dead_plot.setData(self.frame_history, self.dead_history)

    def export(self, granularity_steps, healthy_history, infected_history, recovered_history, dead_history):
        df = pd.DataFrame(list(zip(healthy_history, infected_history, recovered_history,dead_history)), index=granularity_steps, columns=["Gesund", "Infiziert", "Erholt", "Tot"])
        df.index.name = "Zeitschritt"
        export_path = self.choose_export_file()[0]

        if export_path == "":
            pass
        else:
            try:
                df.to_csv(export_path)
            except Exception as e:
                print("Exception occured when exporting file.\n", str(e), "\n\n")

    def refresh_granularity(self): # maybe into view todo
        granularity = self.granularitySlider.value()
        self.granularityLabel.setText(str(granularity))

    def get_granularity(self):
        return self.granularitySlider.value()

    def int_from_input(self, input, standard):
        text = input.text()
        try:
            integer = int(text)
        except Exception as e:
            input.setText(str(standard))
            return standard
        return integer

    def float_from_input(self, input, standard):
        text = input.text()
        try:
            value = float(text)
        except Exception as e:
            input.setText(str(standard))
            return standard
        return value

    def get_simulation_parameters(self):
        particle_count = self.int_from_input(self.countInput, 80)
        infected_count = self.int_from_input(self.infectedInput, 0)
        death_rate = self.int_from_input(self.deathRateInput, DEFAULT_DEATH_RATE) / 100
        infection_time = self.int_from_input(self.infectionTimeInput, DEFAULT_INFECTION_TIME)
        recovered_time = self.int_from_input(self.recoveredTimeInput, DEFAULT_RECOVERED_TIME)
        infection_rate = self.int_from_input(self.infectionRateInput, DEFAULT_INFECTION_RATE) / 100
        return particle_count, infected_count, infection_rate, death_rate, infection_time, recovered_time

    def check_last_drawn(self, current_tick):
        if self.last_drawn_tick < current_tick:
            return True
        else:
            return False

    def get_fps(self):
        if self.fpsInput.text() == "":
            return 60
        else:
            return self.int_from_input(self.fpsInput, 60)


    def get_speed(self):
        print("Speed", self.speedSlider.value() / 100)
        return self.speedSlider.value() / 100

    def get_stepsize(self):
        print(self.stepsizeSlider.value())
        return self.stepsizeSlider.value()

    def get_movement_type(self):
        if self.diagonalRadio.isChecked():
            return Movement.DIAGONAL
        elif self.undirectedRadio.isChecked():
            return Movement.UNDIRECTED
        elif self.directedRadio.isChecked():
            return Movement.DIRECTED

    def get_target_coordinates(self):
            text = self.temporaryCoordinatesInp.text()
            split = text.split(",")
            x = int(split[0])
            y = int(split[1])
            return (x,y)

    def draw_targets(self, targets):
        for target in targets:
            self.scene.addEllipse(target.x,target.y, 15,15, QPen(QColor(235, 226, 52, 255)), QBrush(QColor(235, 226, 52, 255)))