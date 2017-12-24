from math import *
from random import random

class Graph:
    def __init__(self, v, e):
        self.v = v
        self.e = e
        self.vertexArray = []
        self.edgeArray = []

        self.loops = True
        #self.directed = False
        #self.weighted = False
        #self.connected = False


    def makeGraph(self):
        for i in range(self.v):
            self.vertexArray.append(chr(i+97))
        for j in range(self.e):
            edge = []
            #while edge containing both start_vertex and end_vertex doesn't exist in edgeArray (undirected/directed graph)
            #while edge containing both start_vertex and end_vertex IN THAT ORDER doesn't exist in edgeArray (directed multigraph)
            start_vertex = chr(97 + floor(random() * self.v))
            end_vertex = chr(97 + floor(random() * self.v))
            #weight is a gaussian distribution
            weight = 1
            edge.append(start_vertex)
            edge.append(end_vertex)
            edge.append(weight)
            self.edgeArray.append(edge)

    def printGraph(self):
        print ("Vertices: ")
        print(self.vertexArray)
        print ("Edges: ")
        print(self.edgeArray)
