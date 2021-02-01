from view.mainwindow import *
import pyqtgraph as pg
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QFileDialog
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtCore import Qt
import pandas as pd

def check_intersection(ax1, ay1, ax2, ay2, bx1, by1, bx2, by2): # https://silentmatt.com/rectangle-intersection/
    if (ax1 < bx2) and (ax2 > bx1) and (ay1 < by2) and (ay2 > by1):
        return True
    else:
        return False

class View(QtWidgets.QMainWindow, Ui_MainWindow):
    play_pause_simulation_signal = QtCore.pyqtSignal()   # signals do not work in the constructor apparently.
    reset_simulation_signal = QtCore.pyqtSignal()
    export_data_signal = QtCore.pyqtSignal()


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_widgets()
        self.connect_signals()



        self.create_colors()
        self.create_pens()
        self.create_brushes()
        self.set_default_values()

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

    def set_default_values(self):
        self.countInput.setText(str(80))
        self.infectedInput.setText("1")
        self.fpsInput.setText(str(60))
        self.speedInput.setText(str(1))

    def draw_particle(self, x, y, status):
        if status == "h":
            pen = self.pen_healthy
            brush = self.brush_healthy
        elif status == "i":
            pen = self.pen_infected
            brush = self.brush_infected
        elif status == "d":
            pen = self.pen_dead
            brush = self.brush_dead
        elif status == "r":
            pen = self.pen_recovered
            brush = self.brush_recovered
        self.scene.addEllipse(x, y, self.particle_size, self.particle_size, pen, brush)

    def reset_scene(self):
        self.scene.clear()

    def set_scene(self):
        self.view.setScene(self.scene)

    def connect_signals(self):
        self.startBtn.pressed.connect(self.startBtn_clicked)
        self.resetBtn.pressed.connect(lambda: self.reset_simulation_signal.emit())
        self.exportBtn.pressed.connect(lambda: self.export_data_signal.emit())
        self.granularitySlider.valueChanged.connect(self.refresh_granularity)

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


    def draw_particles(self, particles):
        self.reset_scene()
        for particle in particles:
            self.draw_particle(particle.x, particle.y, particle.status)
        self.set_scene()

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
            input.setText(standard)
            return standard
        return integer


    def get_simulation_parameters(self):
        particle_count = self.int_from_input(self.countInput, 80)
        infected_count = self.int_from_input(self.infectedInput, 0)
        death_rate = self.int_from_input(self.deathRateInput, 3) / 100
        infection_time = self.int_from_input(self.infectionTimeInput, 336)
        recovered_time = self.int_from_input(self.recoveredTimeInput, 600)
        return particle_count, infected_count, death_rate, infection_time, recovered_time

    # OLD GRAPH VALUES:
    # def create_infected_plot(self, x, y):
    #     return self.graph.plot(x, y, pen=[255,0,0,255])
    #
    # def create_healthy_plot(self, x, y):
    #     return self.graph.plot(x, y, pen=[0, 255, 33, 255])
    #
    # def create_recovered_plot(self, x, y):
    #     return self.graph.plot(x, y, pen=[12, 0, 193, 255])
    #
    # def create_dead_plot(self, x, y):
    #     return self.graph.plot(x, y, pen=[136, 136, 136, 255])