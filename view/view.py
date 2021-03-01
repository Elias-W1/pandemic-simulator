from view.Mainwindow import *
import pyqtgraph as pg
from PyQt5.QtWidgets import QGraphicsScene, QFileDialog, QSizePolicy, QGraphicsPixmapItem
from PyQt5.QtGui import QColor, QPen, QBrush, QFont, QImage, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRectF
import pandas as pd
from presenter.Constants import *
from view.Constants import *
from model.Constants import *
from view.DiseaseDrawing import *
import pyqtgraph

class View(QtWidgets.QMainWindow, Ui_MainWindow):
    play_pause_simulation_signal = QtCore.pyqtSignal()   # signals do not work in the constructor apparently.
    reset_simulation_signal = QtCore.pyqtSignal()
    export_data_signal = QtCore.pyqtSignal()
    fps_changed_signal = QtCore.pyqtSignal()
    speed_changed_signal = QtCore.pyqtSignal()
    stepsize_changed_signal = QtCore.pyqtSignal()
    movement_changed_signal = QtCore.pyqtSignal()
    measures_changed_signal = QtCore.pyqtSignal()
    resize_signal = QtCore.pyqtSignal()


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.create_widgets()
        self.centralwidget.setLayout(self.mainLayout)

        self.connect_signals()

        self.create_colors()
        self.create_pens()
        self.create_brushes()
        self.set_default_values()
        self.create_fills()

        self.graph.setYRange(0, 1)
        self.graph.setXRange(0,10000)

        self.last_drawn_tick = -1
        self.drawn_diseases = []    # DiseaseDrawing-Objects created from diseases

        self.setWindowTitle(WINDOW_TITLE)
        self.setWindowIcon(QIcon(ICON_IMAGE_PATH))

    def init_stepsize_slider(self):
        self.stepsizeSlider.setMinimum(1)
        self.stepsizeSlider.setMaximum(5)


    def init_speed_slider(self):
        self.speedSlider.setMinimum(10)
        self.speedSlider.setMaximum(500)
        self.speedSlider.setValue(100)

    def create_colors(self):
        self.infected_color = QColor(*INFECTED_COLOR_VALUES)
        self.healthy_color = QColor(*HEALTHY_COLOR_VALUES)
        self.dead_color = QColor(*DEAD_COLOR_VALUES)
        self.recovered_color = QColor(*RECOVERED_COLOR_VALUES)


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

        self.create_scenes()

        # create graph.
        self.graphWidget = pg.PlotWidget()
        self.graphWidget.setBackground('b')

        # Setting values for granularity slider.
        self.granularitySlider.setMinimum(1)
        self.granularitySlider.setMaximum(200)

        self.init_stepsize_slider()
        self.init_speed_slider()

    def create_scenes(self):
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        self.view.show()

        self.mutationScene = QGraphicsScene()
        self.mutationView.setScene(self.mutationScene)
        self.mutationView.show()

    def create_fills(self):
        self.healthy_fill = None
        self.dead_fill = None
        self.recovered_fill = None
        self.infected_fill = None

    def set_default_values(self):
        self.countInput.setText(str(DEFAULT_PARTICLE_COUNT))
        self.infectedInput.setText(str(DEFAULT_INFECTED_COUNT))
        self.fpsInput.setText(str(DEFAULT_FPS))
        self.diseaseNameInp.setText(DEFAULT_DISEASE_NAME)
        self.mutationChanceInp.setText(str(int(DEFAULT_MUTATION_CHANCE*100)))
        self.infectionRateInput.setText(str(int(DEFAULT_INFECTION_RATE*100)))
        self.deathRateInput.setText(str(int(DEFAULT_DEATH_RATE*100)))
        self.infectionTimeInput.setText(str(DEFAULT_INFECTED_DAYS))
        self.recoveredTimeInput.setText(str(DEFAULT_RECOVERED_DAYS))

        self.centerCountInp.setText(str(DEFAULT_VACCINE_CENTER_COUNT))
        self.researchTimeInp.setText(str(DEFAULT_RESEARCH_TIME // TICKS_IN_A_DAY))
        self.effectiveDifferenceInp.setText(str(DEFAULT_DISEASE_DIFFERENCE_EFFECTIVENESS*100))
        self.capacityInp.setText(str(DEFAULT_VACCINE_CENTER_CAPACITY))
        self.restockTimeInp.setText(str(RESTOCK_TIME // TICKS_IN_A_DAY))



    def draw_particle(self, particle):
        drawing_tools = self.select_drawing_tools(particle)
        self.scene.addEllipse(particle.x, particle.y, self.particle_size, self.particle_size, drawing_tools["pen"], drawing_tools["brush"])

    def select_drawing_tools(self, particle):
        status = particle.status
        if status == Status.HEALTHY:
            pen = self.pen_healthy
            brush = self.brush_healthy
        elif status == Status.INFECTED:
            drawn_disease = self.drawn_disease_from_disease(particle.disease)
            pen = drawn_disease.pen
            brush = drawn_disease.brush
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
        self.startBtn.setEnabled(True)
        self.reset_plots()
        self.reset_scene()
        self.reset_status_labels()
        self.last_drawn_tick = -1
        self.mutationScene.clear()
        self.mutationView.setScene(self.mutationScene)
        self.drawn_diseases = []

    def get_measure_parameters(self, maximum):
        # Get mask parameters.
        masked = self.maskCb.isChecked()
        if self.maskDd.currentText() == ABSOLUTE_VALUE_STRING:
            masked_count = self.int_from_input(self.maskInp, 0, maximum, minimum=0)
            masked_percentage = None
        elif self.maskDd.currentText() == PERCENTAGE_VALUE_STRING:
            masked_count = None
            masked_percentage = self.int_from_input(self.maskInp, 0, 100, minimum=0)

        # Get social distancing parameters.
        social_distancing = self.socialDistancingCb.isChecked()
        if self.socialDistancingDd.currentText() == ABSOLUTE_VALUE_STRING:
            sd_count = self.int_from_input(self.socialDistancingInp, 0, maximum, minimum=0)
            sd_percentage = None
        elif self.socialDistancingDd.currentText() == PERCENTAGE_VALUE_STRING:
            sd_count = None
            sd_percentage = self.int_from_input(self.socialDistancingInp, 0, 100, minimum=0)

        # Get vaccine parameters.
        vaccines_enabled = self.vaccinesCb.isChecked()
        center_count = self.int_from_input(self.centerCountInp,DEFAULT_VACCINE_CENTER_COUNT,10,0)
        research_time = self.int_from_input(self.researchTimeInp, DEFAULT_RESEARCH_TIME,minimum=0) * TICKS_IN_A_DAY
        vaccine_effective_percentage_difference = self.int_from_input(self.effectiveDifferenceInp, DEFAULT_DISEASE_DIFFERENCE_EFFECTIVENESS*100,minimum=0)
        vaccine_center_capacity = self.int_from_input(self.capacityInp, DEFAULT_VACCINE_CENTER_CAPACITY,minimum=0)
        vaccine_restock = self.int_from_input(self.restockTimeInp, DEFAULT_VACCINE_CENTER_CAPACITY,minimum=0) * TICKS_IN_A_DAY

        values = {"mask":masked, "masked_count":masked_count, "masked_percentage":masked_percentage,"social_distancing":social_distancing, "social_distancing_count":sd_count, "social_distancing_percentage":sd_percentage, "vaccines":vaccines_enabled,"center_count":center_count, "research_time":research_time,"difference_percentage":vaccine_effective_percentage_difference,"capacity":vaccine_center_capacity,"restock_per_day":vaccine_restock }

        return values


    def connect_signals(self):
        self.startBtn.pressed.connect(self.startBtn_clicked)
        self.resetBtn.pressed.connect(lambda: self.reset_simulation_signal.emit())
        self.exportBtn.pressed.connect(lambda: self.export_data_signal.emit())
        self.granularitySlider.valueChanged.connect(self.refresh_granularity)
        self.speedSlider.valueChanged.connect(lambda: self.speed_changed_signal.emit())
        self.fpsInput.textChanged.connect(lambda: self.fps_changed_signal.emit())
        self.stepsizeSlider.valueChanged.connect(lambda: self.stepsize_changed_signal.emit())
        # Connect speed values changed signal to speed value changes.
        self.diagonalRadio.toggled.connect(lambda: self.movement_changed_signal.emit())
        self.undirectedRadio.toggled.connect(lambda: self.movement_changed_signal.emit())
        # Connect measures changed signal to measure changes.
        self.socialDistancingInp.textChanged.connect(lambda: self.measures_changed_signal.emit())
        self.maskInp.textChanged.connect(lambda: self.measures_changed_signal.emit())
        self.maskDd.currentIndexChanged.connect(lambda: self.measures_changed_signal.emit())
        self.socialDistancingDd.currentIndexChanged.connect(lambda: self.measures_changed_signal.emit())
        self.socialDistancingCb.stateChanged.connect(lambda: self.measures_changed_signal.emit())
        self.maskCb.stateChanged.connect(lambda: self.measures_changed_signal.emit())
        self.vaccinesCb.stateChanged.connect(lambda: self.measures_changed_signal.emit())
        self.centerCountInp.textChanged.connect(lambda: self.measures_changed_signal.emit())
        self.researchTimeInp.textChanged.connect(lambda: self.measures_changed_signal.emit())
        self.effectiveDifferenceInp.textChanged.connect(lambda: self.measures_changed_signal.emit())
        self.capacityInp.textChanged.connect(lambda: self.measures_changed_signal.emit())
        self.restockTimeInp.textChanged.connect(lambda: self.measures_changed_signal.emit())


    def toggle_non_changeable_fields(self):
        current = self.infectionRateInput.isEnabled()
        new = not current
        self.infectionRateInput.setEnabled(new)
        self.deathRateInput.setEnabled(new)
        self.infectionTimeInput.setEnabled(new)
        self.recoveredTimeInput.setEnabled(new)
        self.countInput.setEnabled(new)
        self.infectedInput.setEnabled(new)
        self.diseaseNameInp.setEnabled(new)
        self.mutationCb.setEnabled(new)
        self.mutationChanceInp.setEnabled(new)

    def days_to_ticks(self, ticks):
        return ticks * TICKS_IN_A_DAY

    def startBtn_clicked(self):
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
        self.infected_plot = self.create_infected_plot(self.frame_history, self.infected_history)
        self.healthy_plot = self.create_healthy_plot(self.frame_history, self.healthy_history)
        self.dead_plot = self.create_dead_plot(self.frame_history, self.dead_history)
        self.recovered_plot = self.create_recovered_plot(self.frame_history, self.recovered_history)
        # Create invisible zero and one lines to make stacked graph by filling spaces between real plots and lines.
        self.null_plot = self.graph.plot(self.frame_history, [0], pen=[0,0,0,0])
        self.one_plot = self.graph.plot(self.frame_history, [1], pen=[0,0,0,0])

    def create_infected_plot(self, x, y):
        return  self.graph.plot(x, y, pen=[255,0,0,255])

    def create_healthy_plot(self, x, y):
        return self.graph.plot(x, y, pen=[0, 255, 33, 255])

    def create_recovered_plot(self, x, y):
        return self.graph.plot(x, y, pen=[12, 0, 193, 255])

    def create_dead_plot(self, x, y):
        return self.graph.plot(x, y, pen=[136, 136, 136, 255])

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
        self.graph.removeItem(self.healthy_fill)
        self.graph.removeItem(self.dead_fill)
        self.graph.removeItem(self.recovered_fill)
        self.graph.removeItem(self.infected_fill)

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
        self.scene.addEllipse((particle.x-(particle.infection_abssize//2)), (particle.y-(particle.infection_abssize//2)), self.particle_size + (particle.infection_abssize - 1) , self.particle_size + (particle.infection_abssize - 1), drawing_tools["pen"])

    # Drawing Mutation Tree
    def draw_mutations(self, startdisease, diseaselist):
        self.mutationScene.clear()
        self.diseaselist = diseaselist
        self.update_disease_drawing_list()
        self.draw_mutation_tree(startdisease, 0, 0)
        self.mutationView.setScene(self.mutationScene)

    def draw_mutation(self, drawn_disease, x, y):
        drawn_disease.update()
        texts = []
        texts.append(self.mutationScene.addText(drawn_disease.disease.name))
        texts.append(self.mutationScene.addText("Todesrate: "+str(drawn_disease.disease.death_rate)+" %"))
        texts.append(self.mutationScene.addText("Infektionszeit: " + str(round(drawn_disease.disease.infection_time / TICKS_IN_A_DAY, 1))+" days"))
        texts.append(self.mutationScene.addText("Genesungszeit: " + str(round(drawn_disease.disease.recovery_time / TICKS_IN_A_DAY, 1))+" days"))
        texts.append(self.mutationScene.addText("Mutationswahrscheinlichkeit: " + str(drawn_disease.disease.mutation_chance)+" %"))
        for i in range(len(texts)):
            text = texts[i]
            text.setPos(x+DNA_IMAGE_OFFSET, y+i*TREE_NODE_TEXT_VERTICAL_DISTANCE)
            text.setDefaultTextColor(drawn_disease.color)

        # Drawing DNA Symbol and cross.
        true_y = y+DNA_IMAGE_Y_CORRECTION
        drawn_disease.generate_drawing()
        drawn_disease.dna_pixmap_item.setPos(x, true_y)
        self.mutationScene.addItem(drawn_disease.dna_pixmap_item)

        if drawn_disease.active == False:
            cross_pixmap = self.generate_cross_pixmap()
            cross_pixmap.setPos(x, true_y)
            self.mutationScene.addItem(cross_pixmap)

        if drawn_disease.disease.vaccine_ready:
            vaccine_pixmap = self.generate_vaccine_pixmap()
            vaccine_pixmap.setPos(x+VACCINE_IMAGE_X_OFFSET, true_y+((len(texts)*TREE_NODE_TEXT_VERTICAL_DISTANCE)//2))
            self.mutationScene.addItem(vaccine_pixmap)

        self.mutationScene.addLine(x,y,x,y+TREE_NODE_VERTICAL_LINE_LENGTH)
        self.mutationScene.addLine(x,y+(TREE_NODE_VERTICAL_LINE_LENGTH//2),x+TREE_NODE_CHILD_HORIZONTAL_LINE_LENGTH,y+(TREE_NODE_VERTICAL_LINE_LENGTH//2))
        if drawn_disease.has_children():
            self.mutationScene.addLine(x, y+TREE_NODE_VERTICAL_LINE_LENGTH, x + TREE_NODE_NEXT_CHILD_HORIZONTAL_LINE_LENGTH, y+TREE_NODE_VERTICAL_LINE_LENGTH)

    def generate_cross_pixmap(self):
        image = QImage(CROSS_IMAGE_PATH)
        return QGraphicsPixmapItem(QPixmap.fromImage(image))

    def generate_vaccine_pixmap(self):
        image = QImage(VACCINE_IMAGE_PATH)
        return QGraphicsPixmapItem(QPixmap.fromImage(image))

    def draw_mutation_tree(self, disease, depth, drawn_nodes_count):
        if len(disease.children) == 0 and depth > 0:
            return drawn_nodes_count

        if depth == 0:
            self.draw_mutation(self.drawn_diseases[0], 0, 0)
            drawn_nodes_count = 1
            self.draw_mutation_tree(disease, 1, drawn_nodes_count)
        else:
            for i in range(len(disease.children)):
                child = disease.children[i]
                x = depth * TREE_NODE_HORIZONTAL_DISTANCE
                y = drawn_nodes_count * TREE_NODE_VERTICAL_DISTANCE
                self.draw_mutation(self.drawn_disease_from_disease(child), x, y)
                drawn_nodes_count += 1
                drawn_nodes_count = self.draw_mutation_tree(child, depth+1, drawn_nodes_count)
            return drawn_nodes_count

    def update_status_labels(self, healthy_count, infected_count, recovered_count, dead_count):
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
        # Fills and needed lines.
        self.null_plot.setData(self.frame_history, [0] * len(self.frame_history))
        self.one_plot.setData(self.frame_history, [1] * len(self.frame_history))
        self.update_fills()

    def update_fills(self):
        if self.healthy_fill != None:
            self.graph.removeItem(self.healthy_fill)
            self.healthy_fill = None

        self.healthy_fill = pyqtgraph.FillBetweenItem(self.recovered_plot, self.infected_plot, brush=self.brush_healthy)  # Only use brush on fill else it doesn't fill correctly.
        self.graph.addItem(self.healthy_fill)

        if self.dead_fill != None:
            self.graph.removeItem(self.dead_fill)
            self.dead_fill = None

        self.dead_fill = pyqtgraph.FillBetweenItem(self.one_plot, self.dead_plot, brush=self.brush_dead)
        self.graph.addItem(self.dead_fill)

        if self.infected_fill != None:
            self.graph.removeItem(self.infected_fill)
            self.infected_fill = None

        self.infected_fill = pyqtgraph.FillBetweenItem(self.infected_plot, self.null_plot, brush=self.brush_infected)
        self.graph.addItem(self.infected_fill)

        if self.recovered_fill != None:
            self.graph.removeItem(self.recovered_fill)
            self.recovered_fill = None

        self.recovered_fill = pyqtgraph.FillBetweenItem(self.dead_plot, self.recovered_plot, brush=self.brush_recovered)
        self.graph.addItem(self.recovered_fill)






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

    def refresh_granularity(self):
        granularity = self.granularitySlider.value()
        self.granularityLabel.setText(str(granularity))

    def get_granularity(self):
        return self.granularitySlider.value()

    def int_from_input(self, input, standard, maximum=None, minimum=None):
        text = input.text()
        try:
            integer = int(text)
        except Exception as e:
            input.setText(str(standard))
            return standard

        if maximum != None:
            if integer > maximum:
                input.setText(str(maximum))
                return maximum

        if minimum != None:
            if integer < minimum:
                input.setText(str(minimum))
                return minimum

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
        startdisease_name = self.diseaseNameInp.text()
        particle_count = self.get_particle_count()
        infected_count = self.get_infected_count()
        death_rate = self.int_from_input(self.deathRateInput, DEFAULT_DEATH_RATE, maximum=100, minimum=0) / 100
        infection_time = self.days_to_ticks(self.int_from_input(self.infectionTimeInput, int(DEFAULT_INFECTION_TIME / TICKS_IN_A_DAY), minimum=0))
        recovered_time = self.days_to_ticks(self.int_from_input(self.recoveredTimeInput, int(DEFAULT_RECOVERED_TIME / TICKS_IN_A_DAY), minimum=0))
        infection_rate = self.int_from_input(self.infectionRateInput, DEFAULT_INFECTION_RATE, maximum=100, minimum=0) / 100

        if infected_count > particle_count:
            self.infectedInput.setText(str(particle_count))
            infected_count = particle_count

        mutation_chance = self.int_from_input(self.mutationChanceInp, DEFAULT_MUTATION_CHANCE, maximum=100, minimum=0) / 100
        mutations_enabled = self.mutationCb.isChecked()

        return startdisease_name, particle_count, infected_count, infection_rate, death_rate, infection_time, recovered_time, mutations_enabled, mutation_chance

    def get_particle_count(self):
        return self.int_from_input(self.countInput, 80, minimum=1)

    def set_particle_count(self, count):
        self.countInput.setText(str(count))

    def get_infected_count(self):
        return self.int_from_input(self.infectedInput, 0, minimum=0)

    def set_infected_count(self, count):
        self.infectedInput.setText(str(count))

    def correct_infection_count(self): # corrects starting infected count if it's bigger than whole particle count.
        particle_count = self.get_particle_count()
        if self.get_infected_count() > particle_count:
            self.set_infected_count(particle_count)
            return True
        else:
            return False


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
        return self.speedSlider.value() / 100

    def get_stepsize(self):
        return self.stepsizeSlider.value()

    def get_movement_type(self):
        if self.diagonalRadio.isChecked():
            return Movement.DIAGONAL
        elif self.undirectedRadio.isChecked():
            return Movement.UNDIRECTED

    def get_target_coordinates(self):
            text = self.temporaryCoordinatesInp.text()
            split = text.split(",")
            x = int(split[0])
            y = int(split[1])
            return (x,y)

    def draw_targets(self, targets):
        for target in targets:
            self.scene.addEllipse(target.x-(VACCINE_CENTER_SIZE//2),target.y-(VACCINE_CENTER_SIZE//2), VACCINE_CENTER_SIZE+1, VACCINE_CENTER_SIZE+1, QPen(QColor(235, 226, 52, 255)))

    def simulation_end(self):
        """Gets called when simulation ends because all particles are dead/healthy."""
        self.startBtn.setEnabled(False)
        text = self.scene.addText("Simulation Finished")
        text.setPos(0,0)
        text.setFont(QFont("Impact",25))
        text.setDefaultTextColor(QColor(*SIMULATION_END_TEXT_COLOR))

    def update_disease_drawing_list(self):
        oldlen = len(self.drawn_diseases)
        for i in range(oldlen, len(self.diseaselist)):
                disease = self.diseaselist[i]
                new = DiseaseDrawing(disease)
                self.drawn_diseases.append(new)

    def drawn_disease_from_disease(self, disease):
        return self.drawn_diseases[self.diseaselist.index(disease)]

    def check_diseases_updated(self, diseaselist):
        """Checks if mutation legend must be updated and therefore checks if new diseases mutated, diseases died out, or new vaccines have been developed"""
        if (len(diseaselist) - len(self.drawn_diseases)) > 0:
            return True

        for i in range(len(self.drawn_diseases)):
            if diseaselist[i].active != self.drawn_diseases[i].active:
                return True
            if diseaselist[i].vaccine_ready != self.drawn_diseases[i].vaccine_ready:
                return True

        return False

    def get_simulation_dimensions(self):
        return (self.view.frameGeometry().width(), self.view.frameGeometry().height())

    def resizeEvent(self, event):
        self.resize_signal.emit()
