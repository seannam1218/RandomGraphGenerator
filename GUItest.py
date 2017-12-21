from tkinter import *
from math import *
from random import random
from Graph import *

#constants:
WIDTH = 1000
HEIGHT = 600
X_CENTER = WIDTH/2
Y_CENTER = HEIGHT/2
R = min(WIDTH, HEIGHT)*0.4

VERTEX_RADIUS = 15
VERTEX_COLOR = "#fff"
vertexArray = []
edgeArray = []

root = Tk()
canvas = Canvas(root, width = WIDTH, height = HEIGHT)
vertexPosArray = []

#drawing code goes here
graph = Graph(15, 17)
graph.makeGraph()

def create_edge(x1, y1, x2, y2):
    # atan computes in radians
    if x2-x1 == 0:
        dx = 0
        dy = VERTEX_RADIUS
    elif y2-y1 == 0:
        dx = VERTEX_RADIUS
        dy = 0
    else:
        angle = abs(atan((y2 - y1) / (x2 - x1)))
        print("angle: ")
        print(angle)
        dx = abs(VERTEX_RADIUS * cos(angle))
        print("dx, dy: ")
        print(dx)
        dy = abs(VERTEX_RADIUS * sin(angle))
        print(dy)
    if x1 < x2:
        if y1 < y2:
            canvas.create_line(x1 + dx, y1 + dy, x2 - dx, y2 - dy)
        if y1 >= y2:
            canvas.create_line(x1 + dx, y1 - dy, x2 - dx, y2 + dy)
    if x1 >= x2:
        if y1 < y2:
            canvas.create_line(x1 - dx, y1 + dy, x2 + dx, y2 - dy)
        if y1 >= y2:
            canvas.create_line(x1 - dx, y1 - dy, x2 + dx, y2 + dy)

#x and y are coordinates of the center of vertex.
def create_vertex(name, x, y, r):
    # draw vertices
    canvas.create_oval(x-r, y-r, x+r, y+r, fill = VERTEX_COLOR)
    # draw labels for the vertices
    var = StringVar()
    label = Label(root, textvariable = var,  bg = VERTEX_COLOR)
    var.set(name)
    label.place(x= x-6, y= y-9)

for i in range(0, graph.v):
    v_x = X_CENTER + R * sin(radians(360 * i/graph.v))
    v_y = Y_CENTER - R * cos(radians(360 * i/graph.v))
    v_pos = [v_x, v_y]
    vertexPosArray.append(v_pos)
    create_vertex(graph.vertexArray[i], X_CENTER + R * sin(radians(360 * i/graph.v)), Y_CENTER - R * cos(radians(360 * i/graph.v)), VERTEX_RADIUS)

for e in graph.edgeArray:
    vertex1_index = ord(e[0])-97
    vertex2_index = ord(e[1])-97
    x1 = vertexPosArray[vertex1_index][0]
    y1 = vertexPosArray[vertex1_index][1]
    x2 = vertexPosArray[vertex2_index][0]
    y2 = vertexPosArray[vertex2_index][1]
    create_edge(x1, y1, x2, y2)

graph.printGraph()

canvas.pack()
root.mainloop()