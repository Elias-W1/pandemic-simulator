from presenter.presenter import *
import sys
from PyQt5.QtWidgets import QApplication



# TODO: skalierbarkeit des SimulationsGraphicsView
# TODO: Movement Speed & FPS Speed hinzufügen (oder Doppelter speed anstatt doppelte FPS) (2 Timer und entkoppeln)
# TODO: Mutation
# todo: make rows maximum limit better
# todo: fentser soll skalieren oh man

# todo: grey graphicsview background

# todo: implement measures.

# todo: fix bugs regarding particle size...
# todo: fix stuck particle clusters
# todo: eventuell graph verändern, dass alle Kurven zusammen = 100%
# todo: check graph plotting verbesern

# todo: enum für zustand



if __name__ == '__main__':
    app = QApplication(sys.argv)

    presenter = Presenter()
    presenter.ui.show()

    sys.exit(app.exec_())
