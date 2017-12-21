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
graph = Graph(6, 7)
graph.makeGraph()

# x1,y1,x2,y2, are vertex positions.
def draw_edge(x1, y1, x2, y2):
    if (round(x1, 3) == round(x2, 3)) and (round(y1, 3) == round(y2, 3)):
        canvas.create_arc(x1+15, y1-15, x2+15, y2-15, start = 0, extent = 180)
    else:
        # atan computes in radians
        if round(x2, 3) == round(x1, 3):
            dx = 0
            dy = VERTEX_RADIUS
        elif round(y2, 3) == round(y1, 3):
            dx = VERTEX_RADIUS
            dy = 0
        else:
            angle = abs(atan((y2 - y1) / (x2 - x1)))
            dx = abs(VERTEX_RADIUS * cos(angle))
            dy = abs(VERTEX_RADIUS * sin(angle))

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
def draw_vertex(name, x, y, r):
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
    draw_vertex(graph.vertexArray[i], X_CENTER + R * sin(radians(360 * i/graph.v)), Y_CENTER - R * cos(radians(360 * i/graph.v)), VERTEX_RADIUS)

for e in graph.edgeArray:
    vertex1_index = ord(e[0])-97
    vertex2_index = ord(e[1])-97
    x1 = vertexPosArray[vertex1_index][0]
    y1 = vertexPosArray[vertex1_index][1]
    x2 = vertexPosArray[vertex2_index][0]
    y2 = vertexPosArray[vertex2_index][1]
    draw_edge(x1, y1, x2, y2)

graph.printGraph()

canvas.pack()
root.mainloop()