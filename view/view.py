from view.mainwindow import *
import pyqtgraph as pg
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene
import PyQt5.QtCore
from PyQt5.QtGui import QColor, QPen

class View(QtWidgets.QMainWindow, Ui_MainWindow):
    start_simulation_signal = QtCore.pyqtSignal()   # signals do not work in the constructor apparently.

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_widgets()
        self.connect_signals()
        self.create_pens()

    def set_particle_size(self, particle_size):
        self.particle_size = particle_size

    def create_pens(self):
        self.pen_infected = QPen(QColor(255, 0, 0, 128))
        self.pen_healthy = QPen(QColor(0, 255, 33, 128))

    def create_widgets(self):
        """Initializes widgets."""
        # set 0,0 to bottom left.
        self.view.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignBottom)
        # self.view.setAlignment()

        # create scene (Replaced canvas with GraphicsView).
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.show()

        # create graph.
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('b')
        self.graphWidget.plot(range(10), range(10))

    def draw_particle(self, x, y, status):
        if status == "h":
            pen = self.pen_healthy
        elif status == "i":
            pen = self.pen_infected
        self.scene.addEllipse(x, y, self.particle_size, self.particle_size, pen)

    def reset_scene(self):
        self.scene = None
        self.scene = QGraphicsScene()

    def set_scene(self):
        self.view.setScene(self.scene)

    def connect_signals(self):
        self.startBtn.pressed.connect(self.startBtn_clicked) # lambda usage?

    def startBtn_clicked(self):
        print("Start button pressed.")
        self.start_simulation_signal.emit()

    def set_infectedLabel(self, count):
        self.infectedLabel.setText("{count} Erkrankt.".format(count=count))

    def set_healthyLabel(self, count):
        self.healthyLabel.setText("{count} Gesund.".format(count=count))