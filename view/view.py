from view.mainwindow import *
import pyqtgraph as pg
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QFileDialog
import PyQt5.QtCore
from PyQt5.QtGui import QColor, QPen

class View(QtWidgets.QMainWindow, Ui_MainWindow):
    play_pause_simulation_signal = QtCore.pyqtSignal()   # signals do not work in the constructor apparently.
    reset_simulation_signal = QtCore.pyqtSignal()
    export_data_signal = QtCore.pyqtSignal()
    granularity_changed_signal = QtCore.pyqtSignal()


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_widgets()
        self.connect_signals()

        self.graph.setYRange(0, 1)

        # init colors
        self.infected_color = QColor(255, 0, 0, 128)
        self.healthy_color = QColor(0, 255, 33, 255)
        self.dead_color = QColor(136, 136, 136, 128)
        self.recovered_color = QColor(12, 0, 193, 128)

        self.create_pens()





    def set_particle_size(self, particle_size):
        self.particle_size = particle_size

    def create_pens(self):
        self.pen_infected = QPen(self.infected_color)
        self.pen_healthy = QPen(self.healthy_color)
        self.pen_dead = QPen(self.dead_color)
        self.pen_recovered = QPen(self.recovered_color)

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



    def draw_particle(self, x, y, status):
        if status == "h":
            pen = self.pen_healthy
        elif status == "i":
            pen = self.pen_infected
        elif status == "d":
            pen = self.pen_dead
        elif status == "r":
            pen = self.pen_recovered
        self.scene.addEllipse(x, y, self.particle_size, self.particle_size, pen)

    def reset_scene(self):
        self.scene.clear()

    def set_scene(self):
        self.view.setScene(self.scene)

    def connect_signals(self):
        self.startBtn.pressed.connect(self.startBtn_clicked)
        self.resetBtn.pressed.connect(lambda: self.reset_simulation_signal.emit())
        self.exportBtn.pressed.connect(lambda: self.export_data_signal.emit())
        self.granularitySlider.valueChanged.connect(lambda: self.granularity_changed_signal.emit())

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

    def create_infected_plot(self, x, y):
        return self.graph.plot(x, y, pen=[255,0,0,255])

    def create_healthy_plot(self, x, y):
        return self.graph.plot(x, y, pen=[0, 255, 33, 255])

    def create_recovered_plot(self, x, y):
        return self.graph.plot(x, y, pen=[12, 0, 193, 255])

    def create_dead_plot(self, x, y):
        return self.graph.plot(x, y, pen=[136, 136, 136, 255])

    def get_particle_count(self):
        read = self.countInput.text()
        try:
            integer = int(read)
        except Exception as e:
            self.countInput.setText("80")
            return 80
        return integer

    def get_infected_count(self):
        read = self.infectedInput.text()
        try:
            integer = int(read)
        except Exception as e:
            self.infectedInput.setText("0")
            return 0
        return integer



