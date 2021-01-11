from presenter.presenter import *
import sys
from PyQt5.QtWidgets import QApplication

# TODO: make reset method better
# TODO: make absoulte size value for particle x/y
# TODO: better time complexity ( bis zu 200 Partikel möglich)
# TODO: skalierbarkeit
# TODO: eigener Infektionsradius
# TODO: Movement Speed & FPS Speed hinzufügen (oder Doppelter speed anstatt doppelte FPS)
# TODO: Infektionsradius
# TODO: Nicht jeder Schritt wird angezeigt
# TODO: Mutation
# TODO: Graphen in verschiedenen Farben für mehrere Statistiken
# todo: reset graph at simulation reset (half way there)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    presenter = Presenter()
    presenter.ui.show()

    sys.exit(app.exec_())
