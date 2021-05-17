import sys
from shapeConnection import ShapeHostPoint
from shapeConnection import ShapeJoinPoint
from shapeConnection import ShapeEndPoint
from shapeConnection import ShapeReceiver
from shapeConnection import ShapeSender

def main(mode, file_path, host_name=None):
    # Create SVG/UI class here
    if (mode==0):
        host_point = ShapeHostPoint(simple_rect_handler, simple_circ_handler)
    elif (mode==1):
        join_point = ShapeJoinPoint(host_name, simple_rect_handler, simple_circ_handler)
    else:
        end_point = ShapeEndPoint(host_name, simple_rect_handler, simple_circ_handler)
        end_point.send_rect(0, 0, 1, 1)

def simple_rect_handler(x1, y1, x2, y2):
    print("RECT:", x1, y1, x2, y2)

def simple_circ_handler(x, y, r):
    print("CIRC:", x, y, r)

if __name__ == "__main__" :
    if(len(sys.argv) < 2):
        print("Usage: python3 picto.py <connection_mode> <options...>")
        sys.exit()
    if (sys.argv[1]=="HOST"):
        if(len(sys.argv) != 3):
            print("Usage: python3 picto.py HOST <file_path>")
            sys.exit()
        main(0, sys.argv[2])
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