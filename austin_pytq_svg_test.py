from PyQt5.QtWidgets import QApplication,QMainWindow, QMenuBar, QMenu, QAction, QFileDialog
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *

import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        top = 400
        left = 400
        width = 800
        height = 600
        self.width = width
        self.height = height
        icon = "images/img.png"
        self.icon = icon
        self.setWindowTitle("Paint Test")
        self.setGeometry(top,left,width,height)
        self.setWindowIcon(QIcon(icon))





        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.drawing = False
        self.brushSize =2
        self.brushColor = Qt.black
        self.LastPoint = QPoint()
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        self.brushMenu = mainMenu.addMenu("Brush Size")
        self.brush_color = mainMenu.addMenu("Brush Color")
        self.selectShapes = mainMenu.addMenu("Shapes")

        saveAction =QAction(QIcon(icon),"Save",self)
        saveAction.setShortcut = ("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction(QIcon(icon), "Clear", self)
        clearAction.setShortcut = ("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        endAction = QAction(QIcon(icon), "end", self)
        fileMenu.addAction(endAction)
        endAction.triggered.connect(self.end_painter)

        beginAction = QAction(QIcon(icon), "begin svg", self)
        fileMenu.addAction(beginAction)
        beginAction.triggered.connect(self.start_svg)

        loadAction  = QAction(QIcon(icon), "load svg", self)
        fileMenu.addAction(loadAction)
        loadAction.triggered.connect(self.load_svg)

        self.make_brush_menu()
        self.make_color_menu()
        self.make_shapes_menu()
    def make_brush_menu(self):
        threepxAction = QAction(QIcon(self.icon), "3px", self)
        threepxAction.setShortcut = ("Ctrl+T")
        self.brushMenu.addAction(threepxAction)
        threepxAction.triggered.connect(self.threePx)

        fivepxAction = QAction(QIcon(self.icon), "5px", self)
        fivepxAction.setShortcut = ("Ctrl+F")
        self.brushMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivePx)

        sevenpxAction = QAction(QIcon(self.icon), "7px", self)
        sevenpxAction.setShortcut = ("Ctrl+F")
        self.brushMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenPx)

        ninepxAction = QAction(QIcon(self.icon), "9px", self)
        ninepxAction.setShortcut = ("Ctrl+N")
        self.brushMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninePx)

    def make_color_menu(self):
        blackAction = QAction(QIcon(self.icon), "Black", self)
        blackAction.setShortcut("Ctrl+B")
        self.brush_color.addAction(blackAction)
        blackAction.triggered.connect(self.blackColor)

        whiteAction = QAction(QIcon(self.icon), "White", self)
        whiteAction.setShortcut("Ctrl+W")
        self.brush_color.addAction(whiteAction)
        whiteAction.triggered.connect(self.whiteColor)

        redAction = QAction(QIcon(self.icon), "Red", self)
        redAction.setShortcut("Ctrl+R")
        self.brush_color.addAction(redAction)
        redAction.triggered.connect(self.redColor)

        greenAction = QAction(QIcon(self.icon), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        self.brush_color.addAction(greenAction)
        greenAction.triggered.connect(self.greenColor)

        yellowAction = QAction(QIcon(self.icon), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        self.brush_color.addAction(yellowAction)
        yellowAction.triggered.connect(self.yellowColor)

    def make_shapes_menu(self):
        rectAction = QAction(QIcon(self.icon),"rect",self)
        self.selectShapes.addAction(rectAction)
        rectAction.triggered.connect(self.make_rect)

        ellipsisAction = QAction(QIcon(self.icon),"ellips",self)
        self.selectShapes.addAction(ellipsisAction)
        ellipsisAction.triggered.connect(self.make_elips)

        lineAction =QAction(QIcon(self.icon),"line",self)
        self.selectShapes.addAction(lineAction)
        lineAction.triggered.connect(self.make_line)



    def mousePressEvent(self, event):
        print("work")
        if event.button()  == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            # print(self.lastPoint)
    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            # print("In drawing")
            painter = QPainter(self.image)
            # print("Before painter setPen")
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine,Qt.RoundCap,Qt.RoundJoin))
            # print("Before painter drawLine")
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            print("Before update")
            self.update()
    def mouseReleaseEvent(self, event):
        print("release")
        if event.button == Qt.LeftButton:
            self.drawing = False
    # def paintEvent(self, event):
    #     self.painter = QPainter(self.generator)


    def save(self):
        print("save")
        filePath, __ = QFileDialog.getSaveFileName(self,"Save Image","","PNG(*.png);;JPEG(*.jpg *.jpeg);; ALL Files(*.*)")
        print(filePath)
        if filePath == "":
            return
        self.image.save(filePath)
    def clear(self):
        self.image.fill(Qt.white)
        self.update()



    def make_line(self):
        self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        self.painter.drawLine(0,0,200,200)

    def make_rect(self):
        self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine,Qt.RoundCap,Qt.RoundJoin))
        self.painter.drawRect(40, 40, 400, 400)

    def make_elips(self):
        self.painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine,Qt.RoundCap,Qt.RoundJoin))
        self.painter.drawEllipse(50,50,100,100)

    def start_svg(self):
        self.generator = QSvgGenerator()
        self.generator.setFileName("testing_GUI.svg")
        self.generator.setViewBox(QRect(0, 0, self.width, self.height))
        self.painter = QPainter(self.generator)

    def load_svg(self):
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.viewer = QtSvg.QSvgWidget()
        self.viewer.load('testing_GUI.svg')
        self.viewer.setGeometry(QtCore.QRect(0, 0, 600, 600))
        lay = QtWidgets.QVBoxLayout(self.centralwidget)
        lay.addWidget(self.viewer)

    def end_painter(self):
        self.painter.end()


    def threePx(self):
        self.brushSize =3
    def fivePx(self):
        self.brushSize =5
    def sevenPx(self):
        self.brushSize =7
    def ninePx(self):
        self.brushSize =9
    def blackColor(self):
        self.brushColor = Qt.black
    def redColor(self):
        self.brushColor = Qt.red
    def greenColor(self):
        self.brushColor = Qt.green
    def yellowColor(self):
        self.brushColor = Qt.yellow
    def whiteColor(self):
        self.brushColor = Qt.white




if __name__ == "__main__" :
    # app = QApplication(sys.argv)
    # svgWidget = QSvgWidget('images/castle.svg')
    # svgWidget.setGeometry(50, 50, 759, 668)
    # svgWidget.show()
    #
    # sys.exit(app.exec_())

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()


# main()