from PyQt5.QtWidgets import QApplication,QMainWindow, QMenuBar, QMenu, QAction, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
import sys

class Window(QMainWindow):
    def __init__(self):
        print("Hello")
        super().__init__()
        top = 400
        left = 400
        width = 800
        height = 600
        icon = "images/img.png"
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
        brushMenu = mainMenu.addMenu("Brush Size")
        brushColor = mainMenu.addMenu("Brush Color")

        saveAction =QAction(QIcon("images/img.png"),"Save",self)
        saveAction.setShortcut = ("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction(QIcon("images/img.png"), "Clear", self)
        clearAction.setShortcut = ("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        threepxAction = QAction(QIcon("images/img.png"), "3px", self)
        threepxAction.setShortcut = ("Ctrl+T")
        brushMenu.addAction(threepxAction)
        threepxAction.triggered.connect(self.threePx)

        fivepxAction = QAction(QIcon("images/img.png"), "5px", self)
        fivepxAction.setShortcut = ("Ctrl+F")
        brushMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivePx)

        sevenpxAction = QAction(QIcon("images/img.png"), "7px", self)
        sevenpxAction.setShortcut = ("Ctrl+F")
        brushMenu.addAction(sevenpxAction)
        sevenpxAction.triggered.connect(self.sevenPx)

        ninepxAction = QAction(QIcon("images/img.png"), "9px", self)
        ninepxAction.setShortcut = ("Ctrl+N")
        brushMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninePx)

        blackAction = QAction(QIcon("images/img.png"),"Black",self)
        blackAction.setShortcut("Ctrl+B")
        brushColor.addAction(blackAction)
        blackAction.triggered.connect(self.blackColor)

        whiteAction = QAction(QIcon("images/img.png"), "White", self)
        whiteAction.setShortcut("Ctrl+W")
        brushColor.addAction(whiteAction)
        whiteAction.triggered.connect(self.whiteColor)

        redAction = QAction(QIcon("images/img.png"), "Red", self)
        redAction.setShortcut("Ctrl+R")
        brushColor.addAction(redAction)
        redAction.triggered.connect(self.redColor)

        greenAction = QAction(QIcon("images/img.png"), "Green", self)
        greenAction.setShortcut("Ctrl+G")
        brushColor.addAction(greenAction)
        greenAction.triggered.connect(self.greenColor)

        yellowAction = QAction(QIcon("images/img.png"), "Yellow", self)
        yellowAction.setShortcut("Ctrl+Y")
        brushColor.addAction(yellowAction)
        yellowAction.triggered.connect(self.yellowColor)

    def mousePressEvent(self, event):
        print("work")
        if event.button()  == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()
            # print(self.lastPoint)
    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            print("In drawing")
            painter = QPainter(self.image)
            print("Before painter setPen")
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine,Qt.RoundCap,Qt.RoundJoin))
            print("Before painter drawLine")
            painter.drawLine(self.lastPoint,event.pos())
            self.lastPoint = event.pos()
            print("Before update")
            self.update()
    def mouseReleaseEvent(self, event):
        print("release")
        if event.button == Qt.LeftButton:
            self.drawing = False
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        print("save")
        filePath, __= QFileDialog.getSaveFileName(self,"Save Image","","PNG(*.png);;JPEG(*.jpg *.jpeg);; ALL Files(*.*)")
        print(filePath)
        if filePath == "":
            return
        self.image.save(filePath)
    def clear(self):
        self.image.fill(Qt.white)
        self.update()


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
    print("Hello")
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()


# main()