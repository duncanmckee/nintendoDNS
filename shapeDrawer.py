from PyQt5.QtWidgets import QApplication,QMainWindow, QMenuBar, QMenu, QAction, QFileDialog
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
import shutil

import sys


colors = [Qt.black, Qt.red, Qt.green, Qt.blue, Qt.yellow, Qt.white]

class ShapeDrawer(QMainWindow):
    def __init__(self, shape_point, file_path):
        super().__init__()
        
        self.shape_point = shape_point
        self.shape_point.set_rectangle_handler(self.draw_rectangle)
        self.shape_point.set_ellipse_handler(self.draw_ellipse)
        self.shape_point.set_line_handler(self.draw_line)

        top = 400
        left = 400
        width = 800
        height = 600

        icon = "images/img.png"
        self.setWindowTitle("Nintendo DNS")
        self.setGeometry(top, left, width, height)
        self.setWindowIcon(QIcon(icon))

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        
        self.draw_mode = "none"
        self.preview_shape = "none"

        self.drawing = False
        self.brush_size = 5
        self.brush_color = 0

        # Create menus
        main_menu = self.menuBar()
        # Shapes menu
        shapes_menu = main_menu.addMenu("Shapes")
        rectangle_action = QAction(QIcon(icon),"Rectangle",self)
        rectangle_action.triggered.connect(self.make_rectangle)
        shapes_menu.addAction(rectangle_action)
        ellipse_action = QAction(QIcon(icon),"Ellipse",self)
        ellipse_action.triggered.connect(self.make_ellipse)
        shapes_menu.addAction(ellipse_action)
        line_action = QAction(QIcon(icon),"line",self)
        line_action.triggered.connect(self.make_line)
        shapes_menu.addAction(line_action)
        # Brush size menu
        brush_size_menu = main_menu.addMenu("Brush Size")
        size_three_action = QAction(QIcon(icon),"3 px",self)
        size_three_action.triggered.connect(self.brush_size_three)
        brush_size_menu.addAction(size_three_action)
        size_five_action = QAction(QIcon(icon),"5 px",self)
        size_five_action.triggered.connect(self.brush_size_five)
        brush_size_menu.addAction(size_five_action)
        size_seven_action = QAction(QIcon(icon),"7 px",self)
        size_seven_action.triggered.connect(self.brush_size_seven)
        brush_size_menu.addAction(size_seven_action)
        size_nine_action = QAction(QIcon(icon),"9 px",self)
        size_nine_action.triggered.connect(self.brush_size_nine)
        brush_size_menu.addAction(size_nine_action)
        # Brush color menu
        brush_color_menu = main_menu.addMenu("Brush Color")
        color_black_action = QAction(QIcon(icon),"Black",self)
        color_black_action.triggered.connect(self.brush_color_black)
        brush_color_menu.addAction(color_black_action)
        color_red_action = QAction(QIcon(icon),"Red",self)
        color_red_action.triggered.connect(self.brush_color_red)
        brush_color_menu.addAction(color_red_action)
        color_green_action = QAction(QIcon(icon),"Green",self)
        color_green_action.triggered.connect(self.brush_color_green)
        brush_color_menu.addAction(color_green_action)
        color_blue_action = QAction(QIcon(icon),"Blue",self)
        color_blue_action.triggered.connect(self.brush_color_blue)
        brush_color_menu.addAction(color_blue_action)
        color_yellow_action = QAction(QIcon(icon),"Yellow",self)
        color_yellow_action.triggered.connect(self.brush_color_yellow)
        brush_color_menu.addAction(color_yellow_action)
        color_white_action = QAction(QIcon(icon),"White",self)
        color_white_action.triggered.connect(self.brush_color_white)
        brush_color_menu.addAction(color_white_action)
        

        self.generator = QSvgGenerator()
        self.generator.setFileName(file_path)
        self.generator.setViewBox(QRect(0,0,width,height))
        self.svg_painter = QPainter(self.generator)
        self.svg_painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        self.window_painter = QPainter(self.image)
        self.window_painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
    
    def mousePressEvent(self, event):
        if (event.button() == Qt.LeftButton):
            self.drawing = True
            self.start_point = event.pos()
    def mouseMoveEvent(self, event):
        if (self.drawing):
            self.current_point = event.pos()
            self.preview_shape = self.draw_mode
            self.update()
    def mouseReleaseEvent(self, event):
        if (event.button() == Qt.LeftButton and self.drawing):
            self.drawing = False
            self.preview_shape = "none"
            self.end_point = event.pos()
            if (self.draw_mode == "rectangle"):
                self.shape_point.send_rectangle(self.start_point.x(), self.start_point.y(), self.end_point.x(), self.end_point.y(), self.brush_size, self.brush_color)
            elif (self.draw_mode == "ellipse"):
                self.shape_point.send_ellipse(self.start_point.x(), self.start_point.y(), self.end_point.x(), self.end_point.y(), self.brush_size, self.brush_color)
            elif (self.draw_mode == "line"):
                self.shape_point.send_line(self.start_point.x(), self.start_point.y(), self.end_point.x(), self.end_point.y(), self.brush_size, self.brush_color)
    
    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())
        canvasPainter.setPen(QPen(colors[self.brush_color], self.brush_size-1, Qt.DotLine))
        if(self.preview_shape == "rectangle"):
            canvasPainter.drawRect(QRect(self.start_point, self.current_point))
        elif(self.preview_shape == "ellipse"):
            canvasPainter.drawEllipse(QRect(self.start_point, self.current_point))
        elif(self.preview_shape == "line"):
            canvasPainter.drawLine(QLine(self.start_point, self.current_point))
    
    def closeEvent(self, event):
        print("Shutting down...")
        self.shape_point.close()
        self.svg_painter.end()
        self.window_painter.end()

    # Menu handlers
    # Shape menu handlers
    def make_rectangle(self):
        self.draw_mode = "rectangle"
    def make_ellipse(self):
        self.draw_mode = "ellipse"
    def make_line(self):
        self.draw_mode = "line"
    # Brush size handlers
    def brush_size_three(self):
        self.brush_size = 3
    def brush_size_five(self):
        self.brush_size = 5
    def brush_size_seven(self):
        self.brush_size = 7
    def brush_size_nine(self):
        self.brush_size = 9
    # Brush color handlers
    def brush_color_black(self):
        self.brush_color = 0
    def brush_color_red(self):
        self.brush_color = 1
    def brush_color_green(self):
        self.brush_color = 2
    def brush_color_blue(self):
        self.brush_color = 3
    def brush_color_yellow(self):
        self.brush_color = 4
    def brush_color_white(self):
        self.brush_color = 5

    # Receive shape handlers
    def draw_rectangle(self, x1, y1, x2, y2, width, color):
        bounds = QRect(QPoint(x1, y1), QPoint(x2, y2))
        self.svg_painter.setPen(QPen(colors[color], width, Qt.SolidLine))
        self.svg_painter.drawRect(bounds)
        self.window_painter.setPen(QPen(colors[color], width, Qt.SolidLine))
        self.window_painter.drawRect(bounds)
        self.update()
    
    def draw_ellipse(self, x1, y1, x2, y2, width, color):
        bounds = QRect(QPoint(x1, y1), QPoint(x2, y2))
        self.svg_painter.setPen(QPen(colors[color], width, Qt.SolidLine))
        self.svg_painter.drawEllipse(bounds)
        self.window_painter.setPen(QPen(colors[color], width, Qt.SolidLine))
        self.window_painter.drawEllipse(bounds)
        self.update()
    
    def draw_line(self, x1, y1, x2, y2, width, color):
        bounds = QLine(QPoint(x1, y1), QPoint(x2, y2))
        self.svg_painter.setPen(QPen(colors[color], width, Qt.SolidLine))
        self.svg_painter.drawLine(bounds)
        self.window_painter.setPen(QPen(colors[color], width, Qt.SolidLine))
        self.window_painter.drawLine(bounds)
        self.update()