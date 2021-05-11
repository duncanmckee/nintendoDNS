# https://stackoverflow.com/questions/57432570/generate-a-svg-file-with-pyqt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *

if __name__ == "__main__":
    generator = QSvgGenerator()
    generator.setFileName("created_img.svg")
    generator.setTitle("Making SVGs")
    generator.setSize(QSize(400, 400))
    generator.setViewBox(QRect(0, 0, 400, 400))

    painter = QPainter(generator)
    painter.fillRect(QRect(0, 0, 400, 400), Qt.black)
    painter.setPen(QPen(Qt.red, 8))
    painter.drawRect(40, 40, 200, 100)
    painter.end()

