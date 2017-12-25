from math import *
from random import random

class Graph:
    def __init__(self, v, e, loops):
        self.v = v
        self.e = e
        self.vertexArray = []
        self.edgeArray = []

        self.allow_loops = loops
        self.directed = False
        #self.weighted = False
        #self.connected = False

    def makeGraph(self):
        repeated = False

        for i in range(self.v):
            self.vertexArray.append(chr(i+97))

        j = 1
        while j <= self.e:
            edge = []
            #while edge containing both start_vertex and end_vertex doesn't exist in edgeArray (undirected/directed graph)
            #while edge containing both start_vertex and end_vertex IN THAT ORDER doesn't exist in edgeArray (directed multigraph)
            start_vertex = chr(97 + floor(random() * self.v))
            end_vertex = chr(97 + floor(random() * self.v))
            #weight is a gaussian distribution
            weight = 1

            if self.allow_loops == False:
                if start_vertex == end_vertex:
                    continue

            #check for duplicate edges in UNIGRAPH
            for e in self.edgeArray:
                if (e[0] == start_vertex and e[1] == end_vertex) or (e[0] == end_vertex and e[1] == start_vertex):
                    repeated = True
                    break

            if repeated == True:
                repeated = False
                continue

            edge.append(start_vertex)
            edge.append(end_vertex)
            edge.append(weight)
            self.edgeArray.append(edge)
            j+=1

    def printGraph(self):
        print ("Vertices: ")
        print(self.vertexArray)
        print ("Edges: ")
        print(self.edgeArray)

"""
graph = Graph(4, 5, True)
graph.makeGraph()
graph.printGraph()
"""