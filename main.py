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

    #Listeners to make an action with charge distribution
    def rbRingClicked(self):
        if self.rbRing.isChecked():
            self.flag = 1
            self.lblDimension.setText("Radio (m)")

    def rbLineClicked(self):
        if self.rbLine.isChecked():
            self.flag = 2
            self.lblDimension.setText("Longitud (m)")   

    def rbDiskClicked(self):
        if self.rbDisk.isChecked():
            self.flag = 3
            self.lblDimension.setText("Radio (m)")


    def performResult(self):
        """Function to perform the actions, operations and graphs
        $flag is used to know what's the distribution"""
        self.txtField.setText("")

        self.dimension = float(self.txtDimension.text())
        self.length = float(self.horizontalSlider.value())
        self.charge = float(self.txtPointP_2.text())

        result = 0

        if self.flag == 0:
            #Confirmation of selection
            self.showErrorMessageBox()
        elif self.flag == 1:
            #Ring shape 
            result = self.iRing(self.dimension, self.length, self.charge)
            self.drawRing(result)
            self.graphicsView.setScene(self.scene)
        elif self.flag == 2:
            #Finite line 
            result = self.iChargeLine(self.dimension, self.length, self.charge)
            self.drawLine(result)
            self.graphicsView.setScene(self.scene)
        elif self.flag == 3:
            #Disk distribution
            result = self.iDisk(self.dimension, self.length, self.charge)
            self.drawDisk(result)
            self.graphicsView.setScene(self.scene)
        
        if self.flag != 0:
            self.txtField.setText(str(round(result)))
        
    def showErrorMessageBox(self):
        """Advice to the user to select any distribution"""
        error_message = "La operación no puede ser realizada, elige una distribución de carga"
        QMessageBox.critical(self, "Error", error_message, QMessageBox.Ok)
    
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

    def iChargeLine(self, LLine, PLine, ChLine):
        """Function to calculate the value of the electric field for line distribution"""
        def integrateLine(y, PLine):
            return 1 / ((PLine ** 2) + (y ** 2)) ** (3 / 2)
        
        a = -LLine / 2
        b = LLine / 2

        K = 1 / (4 * self.PI * self.E0)
        result, error = spi.quad(integrateLine, a, b, args=(PLine))
        LambdaR = ChLine / LLine
        cosAlpha = PLine

        value = K * LambdaR * cosAlpha * (result)
        return value

    def iDisk(self, RDisk, LDisk, ChDisk):
        """Function to calculate the value of the electric field for disk distribution"""
        O = ChDisk / (self.PI * RDisk ** 2)
        a = 0
        b = RDisk

        def integrateDisk(r):
            dQ = O * (2 * self.PI * r)
            return (K * dQ * LDisk) / (LDisk ** 2 + r ** 2) ** (3 / 2)

        K = 1 / (4 * self.PI * self.E0)
        value, error = spi.quad(integrateDisk, a, b)

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

    def drawDisk(self, Mfield):
        """Function to graph the disk with the point and field direction"""
        try:
            distance = float(self.horizontalSlider.value())
            sRadius = float(self.txtDimension.text())
            
            self.scene.clear()
            view_center = self.graphicsView.viewport().rect().center()

            ellipse_center = (view_center.x(), view_center.y())
            point_center = (ellipse_center[0] + distance, ellipse_center[1])

            ellipse = QGraphicsEllipseItem(ellipse_center[0] - sRadius, ellipse_center[1] - sRadius * 2, sRadius * 2, sRadius * 4)
            self.scene.addItem(ellipse)
            ellipse_brush = QBrush(QColor(51, 184, 227))
            ellipse.setBrush(ellipse_brush)

            point = QGraphicsEllipseItem(point_center[0] - 2.5, point_center[1] - 2.5, 5, 5)
            brush = QBrush(QColor(0, 0, 0))
            point.setBrush(brush)
            self.scene.addItem(point)

            arrow_start = point_center
            arrow_end = (point_center[0] + Mfield, point_center[1])

            arrow = QGraphicsLineItem(arrow_start[0], arrow_start[1], arrow_end[0], arrow_end[1])
            pen = QPen(QColor(255, 0, 0))
            arrow.setPen(pen)
            self.scene.addItem(arrow)

        except ValueError:
            pass

    def drawLine(self, Mfield):
        """Function to graph the line with the point and field direction"""
        try:
            distance = float(self.horizontalSlider.value())
            sRadius = float(self.txtDimension.text())

            self.scene.clear()
            view_center = self.graphicsView.viewport().rect().center()

            center_x = view_center.x()
            center_y = view_center.y()

            point_x = center_x + distance
            point_y = center_y
            point = QGraphicsEllipseItem(point_x - 2.5, point_y - 2.5, 5, 5)
            brush = QBrush(QColor(0, 0, 0))
            point.setBrush(brush)
            self.scene.addItem(point)

            line_start = (center_x, center_y - sRadius / 2)
            line_end = (center_x, center_y + sRadius / 2)
            line = QGraphicsLineItem(line_start[0], line_start[1], line_end[0], line_end[1])
            pen = QPen(QColor(0, 0, 255))
            line.setPen(pen)
            self.scene.addItem(line)

            arrow_start = (point_x, point_y)
            arrow_end = (arrow_start[0] + Mfield, arrow_start[1])

            arrow = QGraphicsLineItem(arrow_start[0], arrow_start[1], arrow_end[0], arrow_end[1])
            pen = QPen(QColor(255, 0, 0))
            arrow.setPen(pen)
            self.scene.addItem(arrow)

        except ValueError:
            pass

    #Necessary to show the value of the slider in real time.
    def updateLabel(self, value):
        self.lblValue.setText("Value: " + str(value))

if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()