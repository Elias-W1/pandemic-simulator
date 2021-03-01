from PyQt5.QtGui import QColor, QPen, QBrush, QPixmap, QImage
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QGraphicsPixmapItem
from view.Constants import *
from random import randint

class DiseaseDrawing():

    def __init__(self, disease):
        self.disease = disease
        self.color = self.generate_color()
        self.active = True
        self.vaccine_ready = False
        self.generate_drawing_tools()
        self.generate_drawing()


    def update(self):
        if self.active == True and self.disease.infection_count == 0:
            self.color = QColor(*EXTERMINATED_MUTATION_COLOR_VALUES)
            self.active = False
            self.generate_drawing_tools()

        self.vaccine_ready = self.disease.vaccine_ready

    def generate_drawing_tools(self):
        self.brush = QBrush(self.color, Qt.SolidPattern)
        self.pen = QPen(self.color)

    def generate_color(self):
        if self.disease.parent == None:
            return QColor(*INFECTED_COLOR_VALUES)
        else:
            return QColor(255,randint(0,255),0,255)


    def generate_drawing(self):
        self.image = QImage(DNA_IMAGE_PATH)
        self.color_image()
        self.dna_pixmap_item = QGraphicsPixmapItem(QPixmap.fromImage(self.image))

    def color_image(self):
        width = self.image.width()
        height = self.image.height()
        for x in range(width):
            for y in range(height):
                pcolor = self.image.pixelColor(x, y)
                if pcolor.alpha() > 0:
                    self.color.setAlpha(pcolor.alpha())
                    self.image.setPixelColor(x, y, self.color)
        self.color.setAlpha(255)

    def is_initial(self):
        return self.disease.parent == None

    def has_children(self):
        return len(self.disease.children) > 0
