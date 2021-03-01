from presenter.Presenter import *
import sys
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    app = QApplication(sys.argv)

    presenter = Presenter()
    presenter.ui.show()

    sys.exit(app.exec_())
