#!/usr/bin/env python

import numpy as np
import random

# import script for compute heuristic, and show graph
from graph import Graph
from heuristic import Heuristic

"""
######################################
                RRT
######################################
Qgoal //region that identifies success
Counter = 0 //keeps track of iterations
lim = n //number of iterations algorithm should run for
G(V,E) //Graph containing edges and vertices, initialized as empty
While counter < lim:
    Xnew  = RandomPosition()
    if IsInObstacle(Xnew) == True:
        continue
    Xnearest = Nearest(G(V,E),Xnew) //find nearest vertex
    Link = Chain(Xnew,Xnearest)
    G.append(Link)
    if Xnew in Qgoal:
        Return G
Return G
"""

# For call this algorithm ipnuts:
#
#           S_POINT = start point
#           E_POINT = end point
#           GRAPH = searching space, in this case is defined as cube
#           attemps = number of attempts to find path
#           number of iterations = how many times is gen. node
#

# in this algo. is using random generated points
SEED = None

# class where we set up Node with point and parent,
# in pass through RRT algorithm
class Node(object):
    def __init__(self, point, parent):
        self.point = point
        self.parent = parent

# main RRT class, which include self algorithm,
# first is init GRAPH bounderies in searching tree
class RRT(object):
    def __init__(self,GRAPH):
        self.GRAPH = GRAPH

    # method generate point by pseudorandomgenerator,
    # in defined bounderies of graph
    def random_position(self):
        #in this case is the best option to use random.uniform, time to generate number is circus(1.*10-5 to 9.5*10-6)
        position = np.array([random.uniform(self.GRAPH[0],self.GRAPH[1]), random.uniform(self.GRAPH[2], self.GRAPH[3]), random.uniform(self.GRAPH[4], self.GRAPH[5])])
        return position

    # method
    # input: nodes of graph, and searched new point
    # return parrent node of this new point by defined euclidian heuristic
    def search_nearest(self, nodes, new_pos):
        parrent = nodes[0]
        min_dist = Heuristic.euclidan_dist(parrent.point, new_pos)

        for i in range(1, len(nodes)):
            d = Heuristic.euclidan_dist(nodes[i].point, new_pos)
            if min_dist > d:
                min_dist = d
                parrent = nodes[i]

        return parrent

    # method for appned nodes to node list
    # input list of nodes, new point with parent node
    def add_node(self, nodes, point, parent):
        node = Node(point, parent)
        nodes.append(node)

    # method for check if we are in proximity to end point
    # input: goal point, new point
    # Note: for more accurate can be change compute of dist
    def is_goal(self, goal, point):
        dist = Heuristic.euclidan_dist(goal, point)

        if (dist <= 0.01):
            return True
        else:
            return False

# main function
#   input: start point, end point, GRAPH space, attemps, number of iterations
#   return x,y,z coordinates of finded points
# Note: THis is main part of algorithm, in this function is defined
# sequences of RRT algorithm.
def rrt(s_point, e_point, GRAPH, att, N):
    rrt = RRT(GRAPH)
    startnode = Node(s_point, None)

    for i in range(att):
        print("Attempt:" + str(i))
        nodes = []
        nodes.append(startnode)

        random.seed(SEED)

        c = 0
        x, y, z = [], [], []

        while c <= N:
            c += 1
            new_pos = rrt.random_position()
            nearest =  rrt.search_nearest(nodes,new_pos)
            rrt.add_node(nodes, new_pos, nearest)

            if rrt.is_goal(e_point,new_pos):
                print("Path Find!")

                goal_node = nodes[len(nodes)-1]
                currNode = goal_node.parent

                # go back and append points of finded path
                while currNode.parent != None:
                    x.append(currNode.parent.point[0])
                    y.append(currNode.parent.point[1])
                    z.append(currNode.parent.point[2])
                    currNode = currNode.parent

                # append end point
                x.append(currNode.point[0])
                y.append(currNode.point[1])
                z.append(currNode.point[2])

                # classmethod in graph.py for show graph in default web broswer
                Graph.show(x,y,z,"RRT")

                return x,y,z

    # return also if dont find path
    return x,y,z
