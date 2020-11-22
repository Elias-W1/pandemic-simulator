from gui import *
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QApplication
import sys
import pyqtgraph as pg


class Application():
    def __init__(self):
        self.app = QApplication([])
        self.win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.win)
        self.create_widgets()

    def create_widgets(self):
        #Create canvas for drawing
        self.canvas = QtGui.QPixmap(601,601)
        self.ui.drawing.setPixmap(self.canvas)

        #Create graph
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('b')
        self.graphWidget.plot(range(10), range(10))



    def run(self):
        self.win.show()
        sys.exit(self.app.exec_())


app = Application()
app.run()


