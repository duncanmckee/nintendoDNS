from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
import sys


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        #
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        # self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        # self.menubar.setObjectName("menubar")
        # MainWindow.setMenuBar(self.menubar)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)
        #
        # self.retranslateUi(MainWindow)
        # QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #
        self.viewer = QtSvg.QSvgWidget()
        self.viewer.load('images/castle.svg')
        self.viewer.setGeometry(QtCore.QRect(0, 0, 600, 600))
        # self.viewer.setAlignment(self.centralwidget)

        # set the layout to centralWidget
        lay = QtWidgets.QVBoxLayout(self.centralwidget)
        # add the viewer to the layout
        lay.addWidget(self.viewer)

        # MainWindow.setCentralWidget(self.centralwidget)
        # ...

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())