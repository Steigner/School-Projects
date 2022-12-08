#!/usr/bin/env python

# import script for compute heuristic, and show graph
from graph import Graph
from heuristic import Heuristic

"""
######################################
                A*
######################################
function reconstruct_path(cameFrom, current)
    total_path := {current}
    while current in cameFrom.Keys:
        current := cameFrom[current]
        total_path.prepend(current)
    return total_path
function A_Star(start, goal, h)
    openSet := {start}
    cameFrom := an empty map
    gScore := map with default value of Infinity
    gScore[start] := 0
    fScore := map with default value of Infinity
    fScore[start] := h(start)
    while openSet is not empty
        current := the node in openSet having the lowest fScore[] value
        if current = goal
            return reconstruct_path(cameFrom, current)
        openSet.Remove(current)
        for each neighbor of current
            tentative_gScore := gScore[current] + d(current, neighbor)
            if tentative_gScore < gScore[neighbor]
                cameFrom[neighbor] := current
                gScore[neighbor] := tentative_gScore
                fScore[neighbor] := gScore[neighbor] + h(neighbor)
                if neighbor not in openSet
                    openSet.add(neighbor)
    return failure
"""

# Becouse A* is informed algorithm, it is neccesery to create Graph as space.
# Power of this algorithm is, if exist any solution, he will find him, becouse
# comes out from Dijkstra algorithm. This implementation of A* algorithm isnt the most optimalized
# version of A*.
#
# For call this algorithm ipnuts:
#
#           S_POINT = start point
#           E_POINT = end point
#           GRAPH = searching space, in this case is defined as cube
#           subdivision = this should subdivided working space on Graph(V,E) represented of int E.
#

# In this class is defined how many rows and column need to be allocate.
# It will be maybe little bit confuse, but row represent "line" in x,y,z coordinates.
class Space(object):
    def __init__(self, row_x, row_y, row_z, total_rows_x, total_rows_y, total_rows_z):
        self.row_x = row_x
        self.row_y = row_y
        self.row_z = row_z

        self.x = row_x
        self.y = row_y
        self.z = row_z

        self.total_rows_x = total_rows_x
        self.total_rows_y = total_rows_y
        self.total_rows_z = total_rows_z

        self.neighbors = None

    # this method update allocated grid and create informed space,
    # if neigbour is obstacle or if can be use as part of path
    def update_neighbors(self, grid):
        self.neighbors = []

        if self.row_x < self.total_rows_x - 1:
            self.neighbors.append(grid[self.row_x + 1][self.row_y][self.row_z])

        if self.row_x > 0:
            self.neighbors.append(grid[self.row_x - 1][self.row_y][self.row_z])

        if self.row_y < self.total_rows_y - 1:
            self.neighbors.append(grid[self.row_x][self.row_y + 1][self.row_z])

        if self.row_y > 0:
            self.neighbors.append(grid[self.row_x][self.row_y - 1][self.row_z])

        if self.row_z < self.total_rows_z - 1:
            self.neighbors.append(grid[self.row_x][self.row_z][self.row_z+1])

        if self.row_z > 0:
            self.neighbors.append(grid[self.row_x][self.row_z][self.row_z-1])

    # get position from space, so position in Graph
    def get_pos(self):
        return self.row_x, self.row_y, self.row_z

class A_star(object):
    def __init__(self):
        self.grid = []
        self.open_set = []
        self.g_score = []
        self.f_score = []
        self.close_set = []

    # this method might be a little bit slower then others from programs on Github
    # and on another implementation on internet, but this represent how can be done another way
    # then by using dicts
    def score_space(self):
        grid = self.grid

        for x in range(len(grid)):
            self.g_score.append([])
            self.f_score.append([])
            self.close_set.append([])

            for y in range(len(grid[:])):
                self.g_score[x].append([])
                self.f_score[x].append([])
                self.close_set[x].append([])

                # for every cell, set inf -> as pseudocode
                # clouset is set with same logic, for determine path
                for z in range(len(grid[:][:])):
                    self.g_score[x][y].append(float("inf"))
                    self.f_score[x][y].append(float("inf"))
                    self.close_set[x][y].append([])

    # main method, self algorithm
    #   input: start point, end point, graph, subdivision
    #   return finded path points
    def algorithm(self, start, end, GRAPH, subdiv):
        open_set = self.open_set
        close_set = self.close_set
        g_score = self.g_score
        f_score = self.f_score

        # init lists of coordinates x,y,z of finded path, if path is not find, then
        # are returned empty lists
        x, y, z = [], [], []

        self.score_space()

        # gScore[start] is the cost of the cheapest path from start to currently known
        g_score[start.x][start.y][start.z] = 0
        # for start node, fScore[start] = gScore[start] + h(start). fScore[star] represents our current best guess as to
        # how short path from start to finish can be
        f_score[start.x][start.y][start.z] = Heuristic.euclidan_dist(start.get_pos(), end.get_pos())

        # first is append start node
        open_set.append(start)

        while open_set:

            current = open_set[0]

            for node in open_set:
                if f_score[node.x][node.y][node.z] < f_score[current.x][current.y][current.z]:
                    current = node

            # if is finded path, we find in close_set and append x,y,z coordinates, for
            # using in motion_planning.py script.
            if current == end:
                print("Path Find!")
                for i in range(len(close_set)):
                    current = close_set[current.x][current.y][current.z]
                    x.append(current.x/float(subdiv)+GRAPH[0])
                    y.append((current.y/float(subdiv))+GRAPH[2])
                    z.append((current.z/float(subdiv))+GRAPH[4])

                    # if we get start node, we can break loop
                    if start.x == current.x and start.y == current.y and start.z == current.z:
                        break

                return x,y,z

            open_set.remove(current)

            for neighbor in current.neighbors:
                # d(current,neighbor) is the weight of the edge from current to neighbor
                # tentative_gScore is the distance from start to the neighbor through current
                temp_g_score = g_score[current.x][current.y][current.z] + Heuristic.euclidan_dist(current.get_pos(), neighbor.get_pos())

                if temp_g_score < g_score[neighbor.x][neighbor.y][neighbor.z]:
                    close_set[neighbor.x][neighbor.y][neighbor.z] = current
                    g_score[neighbor.x][neighbor.y][neighbor.z] = temp_g_score
                    f_score[neighbor.x][neighbor.y][neighbor.z] = temp_g_score + Heuristic.euclidan_dist(neighbor.get_pos(), end.get_pos())

                    # This path to neighbor is better than any previous one. Record it!
                    if neighbor not in open_set:
                        open_set.append(neighbor)

        return x, y, z

    # method calculate and allocate Graph
    #   input: subdiveded graph
    #   return allocated graph space
    # Note: first of is defined size of space
    # then, is in for loops create nodes
    def make_grid(self, graph):
        row_x = graph[1] - graph[0]
        row_y = graph[3] - graph[2]
        row_z = graph[5] - graph[4]

        for x in range(row_x):
            self.grid.append([])

            for y in range(row_y):
                self.grid[x].append([])

                for z in range(row_z):
                    cell = Space(x , y, z, row_x, row_y, row_z)
                    self.grid[x][y].append(cell)

        for row_x in self.grid:
            for row_y in row_x:
                for row_z in row_y:
                    row_z.update_neighbors(self.grid)

        return self.grid

# main function
#   input: start point, end point, GRAPH space, subdivision number
#   return x,y,z coordinates of finded points
# Note: first subdivision and prepare start point and end point, then create
# work space, and put it to a star algorithm
def a_star(s_point, e_point, GRAPH, subdiv):
    astar = A_star()

    # this is pre-prepare part, for subdivision of working space to
    # int Graph(V,E). For this purpose it also need be changed start and
    # end point.
    graph = [int(round(i*subdiv)) for i in GRAPH]
    s_point = [int(round(i*subdiv)) for i in s_point]
    e_point = [int(round(i*subdiv)) for i in e_point]

    s_point[0] = s_point[0] - graph[0]
    s_point[1] = s_point[1] - graph[2]
    s_point[2] = s_point[2] - graph[4]

    e_point[0] = e_point[0] - graph[0]
    e_point[1] = e_point[1] - graph[2]
    e_point[2] = e_point[2] - graph[4]

    # call make grid for allocate Graph of working space
    grid = astar.make_grid(graph)
    start_cell = grid[s_point[0]][s_point[1]][s_point[2]]
    end_cell = grid[e_point[0]][e_point[1]][e_point[2]]

    # call computing of algorithm
    x, y, z = astar.algorithm(start_cell, end_cell, GRAPH, subdiv)

    # classmethod in graph.py for show graph in default web broswer
    Graph().show(x,y,z,"A*")

    return x,y,z
