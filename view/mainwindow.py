# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1270, 931)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graph = PlotWidget(self.centralwidget)
        self.graph.setGeometry(QtCore.QRect(50, 150, 521, 481))
        self.graph.setObjectName("graph")
        self.healthyLabel = QtWidgets.QLabel(self.centralwidget)
        self.healthyLabel.setGeometry(QtCore.QRect(50, 132, 521, 16))
        self.healthyLabel.setStyleSheet("color: rgb(0, 158, 37);\n"
"")
        self.healthyLabel.setObjectName("healthyLabel")
        self.infectedLabel = QtWidgets.QLabel(self.centralwidget)
        self.infectedLabel.setGeometry(QtCore.QRect(50, 118, 521, 16))
        self.infectedLabel.setStyleSheet("color: rgb(226, 0, 0);")
        self.infectedLabel.setObjectName("infectedLabel")
        self.recoveredLabel = QtWidgets.QLabel(self.centralwidget)
        self.recoveredLabel.setGeometry(QtCore.QRect(50, 104, 521, 16))
        self.recoveredLabel.setStyleSheet("color: rgb(12, 0, 193);")
        self.recoveredLabel.setObjectName("recoveredLabel")
        self.deadLabel = QtWidgets.QLabel(self.centralwidget)
        self.deadLabel.setGeometry(QtCore.QRect(50, 90, 521, 16))
        self.deadLabel.setStyleSheet("color: rgb(136, 136, 136);")
        self.deadLabel.setObjectName("deadLabel")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(550, 630, 21, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(0, 150, 51, 51))
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setObjectName("label_6")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(30, 720, 1231, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.countInput = QtWidgets.QLineEdit(self.centralwidget)
        self.countInput.setGeometry(QtCore.QRect(30, 760, 141, 20))
        self.countInput.setObjectName("countInput")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(30, 740, 141, 16))
        self.label_7.setObjectName("label_7")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(210, 730, 16, 151))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.socialDistancingCb = QtWidgets.QCheckBox(self.centralwidget)
        self.socialDistancingCb.setGeometry(QtCore.QRect(230, 730, 101, 17))
        self.socialDistancingCb.setObjectName("socialDistancingCb")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(230, 790, 131, 21))
        self.label.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"color: rgb(211, 211, 211);")
        self.label.setObjectName("label")
        self.socialDistancingInp = QtWidgets.QLineEdit(self.centralwidget)
        self.socialDistancingInp.setGeometry(QtCore.QRect(240, 770, 113, 20))
        self.socialDistancingInp.setObjectName("socialDistancingInp")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(240, 750, 81, 16))
        self.label_2.setObjectName("label_2")
        self.socialDistancingDd = QtWidgets.QComboBox(self.centralwidget)
        self.socialDistancingDd.setGeometry(QtCore.QRect(360, 770, 69, 22))
        self.socialDistancingDd.setObjectName("socialDistancingDd")
        self.socialDistancingDd.addItem("")
        self.socialDistancingDd.addItem("")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(360, 750, 71, 16))
        self.label_3.setObjectName("label_3")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(1060, 730, 16, 81))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.startBtn = QtWidgets.QPushButton(self.centralwidget)
        self.startBtn.setGeometry(QtCore.QRect(1080, 760, 111, 31))
        self.startBtn.setObjectName("startBtn")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(1080, 730, 171, 21))
        self.label_4.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"color: rgb(211, 211, 211);")
        self.label_4.setObjectName("label_4")
        self.groupLabel = QtWidgets.QLabel(self.centralwidget)
        self.groupLabel.setGeometry(QtCore.QRect(10, 0, 261, 21))
        self.groupLabel.setStyleSheet("font: 87 14pt \"Arial Black\";\n"
"color: rgb(211, 211, 211);")
        self.groupLabel.setObjectName("groupLabel")
        self.view = QtWidgets.QGraphicsView(self.centralwidget)
        self.view.setGeometry(QtCore.QRect(660, 30, 600, 600))
        self.view.setObjectName("view")
        self.infectedInput = QtWidgets.QLineEdit(self.centralwidget)
        self.infectedInput.setGeometry(QtCore.QRect(30, 810, 141, 20))
        self.infectedInput.setObjectName("infectedInput")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(30, 790, 141, 16))
        self.label_8.setObjectName("label_8")
        self.fpsInput = QtWidgets.QLineEdit(self.centralwidget)
        self.fpsInput.setGeometry(QtCore.QRect(930, 760, 113, 20))
        self.fpsInput.setObjectName("fpsInput")
        self.speedInput = QtWidgets.QLineEdit(self.centralwidget)
        self.speedInput.setGeometry(QtCore.QRect(930, 820, 113, 20))
        self.speedInput.setObjectName("speedInput")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(930, 740, 61, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(930, 800, 141, 20))
        self.label_10.setObjectName("label_10")
        self.resetBtn = QtWidgets.QPushButton(self.centralwidget)
        self.resetBtn.setGeometry(QtCore.QRect(1200, 760, 51, 31))
        self.resetBtn.setObjectName("resetBtn")
        self.exportBtn = QtWidgets.QPushButton(self.centralwidget)
        self.exportBtn.setGeometry(QtCore.QRect(50, 650, 75, 23))
        self.exportBtn.setObjectName("exportBtn")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(910, 730, 16, 151))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self.centralwidget)
        self.line_5.setGeometry(QtCore.QRect(720, 730, 16, 151))
        self.line_5.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(730, 730, 141, 16))
        self.label_11.setObjectName("label_11")
        self.deathRateInput = QtWidgets.QLineEdit(self.centralwidget)
        self.deathRateInput.setGeometry(QtCore.QRect(730, 750, 141, 20))
        self.deathRateInput.setObjectName("deathRateInput")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(880, 750, 21, 16))
        self.label_12.setObjectName("label_12")
        self.infectionTimeInput = QtWidgets.QLineEdit(self.centralwidget)
        self.infectionTimeInput.setGeometry(QtCore.QRect(730, 800, 141, 20))
        self.infectionTimeInput.setObjectName("infectionTimeInput")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(730, 780, 141, 16))
        self.label_13.setObjectName("label_13")
        self.recoveredTimeInput = QtWidgets.QLineEdit(self.centralwidget)
        self.recoveredTimeInput.setGeometry(QtCore.QRect(730, 850, 141, 20))
        self.recoveredTimeInput.setObjectName("recoveredTimeInput")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(730, 830, 141, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(880, 800, 31, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(880, 850, 31, 16))
        self.label_16.setObjectName("label_16")
        self.granularitySlider = QtWidgets.QSlider(self.centralwidget)
        self.granularitySlider.setGeometry(QtCore.QRect(160, 660, 160, 22))
        self.granularitySlider.setOrientation(QtCore.Qt.Horizontal)
        self.granularitySlider.setObjectName("granularitySlider")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(160, 640, 71, 16))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(160, 680, 16, 16))
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19.setGeometry(QtCore.QRect(300, 680, 21, 20))
        self.label_19.setObjectName("label_19")
        self.granularityLabel = QtWidgets.QLabel(self.centralwidget)
        self.granularityLabel.setGeometry(QtCore.QRect(230, 640, 61, 16))
        self.granularityLabel.setText("")
        self.granularityLabel.setObjectName("granularityLabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1270, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Pandemie Simulator"))
        self.healthyLabel.setText(_translate("MainWindow", "000 Gesund"))
        self.infectedLabel.setText(_translate("MainWindow", "000 Infiziert"))
        self.recoveredLabel.setText(_translate("MainWindow", "000 Genesen"))
        self.deadLabel.setText(_translate("MainWindow", "000 Gestorben"))
        self.label_5.setText(_translate("MainWindow", "Zeit"))
        self.label_6.setText(_translate("MainWindow", "Anteil \n"
"Menschen \n"
"in %"))
        self.label_7.setText(_translate("MainWindow", "Gesamtzahl Menschen"))
        self.socialDistancingCb.setText(_translate("MainWindow", "Social Distancing"))
        self.label.setText(_translate("MainWindow", "Maßnahmen"))
        self.label_2.setText(_translate("MainWindow", "Menschen"))
        self.socialDistancingDd.setItemText(0, _translate("MainWindow", "Anzahl"))
        self.socialDistancingDd.setItemText(1, _translate("MainWindow", "%"))
        self.label_3.setText(_translate("MainWindow", "Anzahl / %"))
        self.startBtn.setText(_translate("MainWindow", "Start"))
        self.label_4.setText(_translate("MainWindow", "Start Simulation"))
        self.groupLabel.setText(_translate("MainWindow", "Gruppe mit Maßnahmen"))
        self.label_8.setText(_translate("MainWindow", "Anfänglich Infizierte"))
        self.label_9.setText(_translate("MainWindow", "FPS"))
        self.label_10.setText(_translate("MainWindow", "Simulationsgeschwindigkeit"))
        self.resetBtn.setText(_translate("MainWindow", "Reset"))
        self.exportBtn.setText(_translate("MainWindow", "Exportieren"))
        self.label_11.setText(_translate("MainWindow", "Todesrate"))
        self.deathRateInput.setText(_translate("MainWindow", "3"))
        self.label_12.setText(_translate("MainWindow", "%"))
        self.infectionTimeInput.setText(_translate("MainWindow", "336"))
        self.label_13.setText(_translate("MainWindow", "Genesungszeit"))
        self.recoveredTimeInput.setText(_translate("MainWindow", "600"))
        self.label_14.setText(_translate("MainWindow", "Immunzeit"))
        self.label_15.setText(_translate("MainWindow", "ticks"))
        self.label_16.setText(_translate("MainWindow", "ticks"))
        self.label_17.setText(_translate("MainWindow", "Granularität:"))
        self.label_18.setText(_translate("MainWindow", "1"))
        self.label_19.setText(_translate("MainWindow", "200"))
from pyqtgraph import PlotWidget
