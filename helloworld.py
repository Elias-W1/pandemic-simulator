from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QWidget, QApplication
import sys

print("Hello World!")

class HelloWorld(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        label = QLabel("Hello World!")
        self.setCentralWidget(label)


app = QApplication([])
win = HelloWorld()
win.show()
sys.exit(app.exec_())