import numpy
import scipy.integrate as spi
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QMessageBox,
    QGraphicsEllipseItem,
    QGraphicsLineItem,
    QGraphicsScene,
)
from PyQt5.QtGui import QColor, QBrush, QPen
from PyQt5 import uic

class MyWindow(QMainWindow):

    PI = numpy.pi
    E0 = 8.854187817e-12

    def __init__(self):
        super().__init__()
        uic.loadUi("GraphicInterface.ui", self)

        self.flag = 0
        self.scene = QGraphicsScene(self)

        self.rbRing.clicked.connect(self.rbRingClicked)
        self.rbLine.clicked.connect(self.rbLineClicked)
        self.rbDisk.clicked.connect(self.rbDiskClicked)
        self.horizontalSlider.valueChanged.connect(self.updateLabel)
        self.btnCalculate.clicked.connect(self.performResult)

        # Initialize instance variables
        self.dimension = 0.0
        self.length = 0.0
        self.charge = 0.0

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()