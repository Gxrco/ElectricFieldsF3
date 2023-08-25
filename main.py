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

    def iRing(self, RRing, LRing, ChRing):
        """Function to calculate the value of the electric field for ring distribution"""
        def integrateRing(D):
            return 1
        
        a = 0
        b = 2 * self.PI * RRing

        K = 1 / (4 * self.PI * self.E0)
        #Capture just magnitude
        result, error = spi.quad(integrateRing, a, b)
        LambdaR = ChRing / (2 * self.PI * RRing)
        cosAlpha = (LRing / (LRing ** 2 + RRing ** 2) ** (1 / 2))

        value = K * LambdaR * cosAlpha * (1 / (LRing ** 2 + RRing ** 2)) * (result)
        return value


    def drawRing(self, Mfield):
        """Function to graph the ring with the point and field direction"""
        try:
            distance = float(self.horizontalSlider.value())
            sRadius = float(self.txtDimension.text())
            
            self.scene.clear()
            view_center = self.graphicsView.viewport().rect().center()

            ellipse_center = (view_center.x(), view_center.y())
            point_center = (ellipse_center[0] + distance, ellipse_center[1])

            point = QGraphicsEllipseItem(point_center[0] - 2.5, point_center[1] - 2.5, 5, 5)
            brush = QBrush(QColor(0, 0, 0))
            point.setBrush(brush)
            self.scene.addItem(point)

            ellipse = QGraphicsEllipseItem(ellipse_center[0] - sRadius, ellipse_center[1] - sRadius * 2, sRadius * 2, sRadius * 4)
            self.scene.addItem(ellipse)

            arrow_start = point_center
            arrow_end = (point_center[0] + Mfield, point_center[1])

            arrow = QGraphicsLineItem(arrow_start[0], arrow_start[1], arrow_end[0], arrow_end[1])
            pen = QPen(QColor(255, 0, 0))
            arrow.setPen(pen)
            self.scene.addItem(arrow)

        except ValueError:
            pass

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()