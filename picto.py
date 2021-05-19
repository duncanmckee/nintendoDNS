import sys
import threading
from PyQt5.QtWidgets import QApplication
from shapeDrawer import ShapeDrawer
from shapeConnection import ShapeHostPoint
from shapeConnection import ShapeJoinPoint
from shapeConnection import ShapeEndPoint
from shapeConnection import ShapeReceiver
from shapeConnection import ShapeSender

def main(mode, file_path, host_name):
    if (mode==0):
        point = ShapeHostPoint(host_name)
    elif (mode==1):
        point = ShapeJoinPoint(host_name)
    else:
        point = ShapeEndPoint(host_name)
    app = QApplication([])
    drawer = ShapeDrawer(point, file_path)
    drawer.show()
    app.exec()

if __name__ == "__main__" :
    if(len(sys.argv) < 2):
        print("Usage: python3 picto.py <connection_mode> <options...>")
        sys.exit()
    if (sys.argv[1]=="HOST"):
        if(len(sys.argv) != 4):
            print("Usage: python3 picto.py HOST <file_path> <host_name>")
            sys.exit()
        main(0, sys.argv[2], sys.argv[3])
    elif (sys.argv[1]=="JOIN"):
        if(len(sys.argv) != 4):
            print("Usage: python3 picto.py JOIN <file_path> <host_name>")
            sys.exit()
        main(1, sys.argv[2], sys.argv[3])
    elif (sys.argv[1]=="END"):
        if(len(sys.argv) != 4):
            print("Usage: python3 picto.py END <file_path> <host_name>")
            sys.exit()
        main(2, sys.argv[2], sys.argv[3])
    else:
        print("Error: Unsupported connection_mode (supported modes: HOST, JOIN, END)")
        sys.exit()