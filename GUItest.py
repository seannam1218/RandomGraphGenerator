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

#drawing code goes here
graph = Graph(13, 12)
graph.makeGraph()

def create_edge(x1, y1, x2, y2):
    canvas.create_line(x1, y1, x2, y2)
#x and y are coordinates of the center of vertex.
def create_vertex(name, x, y, r):
    canvas.create_oval(x-r, y-r, x+r, y+r, fill = VERTEX_COLOR)
def create_vertex_labels(name, x, y):
    var = StringVar()
    label = Label(root, textvariable = var,  bg = VERTEX_COLOR)
    var.set(name)
    label.place(x= x, y= y)

for i in range(0, graph.v):
    create_vertex(graph.vertexArray[i], X_CENTER + R * sin(radians(360 * i/graph.v)), Y_CENTER - R * cos(radians(360 * i/graph.v)), VERTEX_RADIUS)


graph.printGraph()

canvas.pack()
root.mainloop()