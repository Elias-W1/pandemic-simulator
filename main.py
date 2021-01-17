from presenter.presenter import *
import sys
from PyQt5.QtWidgets import QApplication


# TODO: make absoulte size value for particle x/y
# TODO: better time complexity ( bis zu 200 Partikel möglich)
# TODO: skalierbarkeit des SimulationsGraphicsView
# TODO: eigener Infektionsradius
# TODO: Movement Speed & FPS Speed hinzufügen (oder Doppelter speed anstatt doppelte FPS)
# TODO: Mutation
# todo: make rows maximum limit better
# todo: klassen auf files aufteilen
# todo: fentser soll skalieren oh man
# todo: make robust get input from LineEdit function
# todo: eventuell graph verändern, dass alle Kurven zusammen = 100%



if __name__ == '__main__':
    app = QApplication(sys.argv)

    presenter = Presenter()
    presenter.ui.show()

    sys.exit(app.exec_())
