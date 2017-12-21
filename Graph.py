from math import *
from random import random

class Graph:
    def __init__(self, v, e):
        self.v = v
        self.e = e
        self.vertexArray = []
        self.edgeArray = []

        self.cycles = True
        #self.directed = False
        #self.weighted = False
        #self.connected = False


    def makeGraph(self):
        for i in range(self.v):
            self.vertexArray.append(chr(i+97))
        for j in range(self.e):
            edge = []
            a = chr(97 + floor(random() * self.v))
            b = chr(97 + floor(random() * self.v))
            weight = 1
            edge.append(a)
            edge.append(b)
            edge.append(weight)
            self.edgeArray.append(edge)

    def printGraph(self):
        print ("Vertices: ")
        print(self.vertexArray)
        print ("Edges: ")
        print(self.edgeArray)
