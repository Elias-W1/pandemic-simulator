from presenter.Presenter import *
import sys
from PyQt5.QtWidgets import QApplication



# TODO: skalierbarkeit des SimulationsGraphicsView
# todo: fentser soll skalieren oh man

# todo: grey graphicsview background


# todo: fix bugs regarding particle size...
# todo: fix stuck particle clusters
# todo: eventuell graph verändern, dass alle Kurven zusammen = 100%
# todo: graph update methode fixen | Graph und fps entkoppeln

# todo: DRAWING starts not at middle point but at xy! !! !! !!!!!!!
#todo mutation factor CONSTANTS

# todo: Mutations Legende
# todo: verschiedene Farben für Mutationen
# todo: name base for mutations
# todo mutation chance from gui

# todo: infection radius reduction implementieren

# ## ### ## Meilenstein #### # ## ## ## # ##


# added: Partikel werden an zufälligen Positionen gespawnt
# added: Status, Movement Typ enum
# added: Constant files für model, view, presenter
# added: Mutationen & Disease Klasse
# added: Einstellung von Geschwindigkeit, FPS, Schrittgröße
# Partikelmaximum-Berechnung verbessert.
# added: infection radius um partikel wenn ein infiziertes Partikel auf ein anderes Partikel trifft
# added: Einfaches social distancing, das noch nicht perfekt ist
# added: Masken, die Infektionswahrscheinlichkeit bei Kontakt deutlich reduzieren
# added: ungerichtete Bewegung
# added rudimentäre gerichtete Bewegung inklusive Zielklasse,


if __name__ == '__main__':
    app = QApplication(sys.argv)

    presenter = Presenter()
    presenter.ui.show()

    sys.exit(app.exec_())
