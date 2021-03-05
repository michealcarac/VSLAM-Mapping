# ------------------------------------------------------------------------------
# Name           : AStarOCC.py
# Date Created   : 2/26/2021
# Author(s)      : Micheal Caracciolo, Chris Lloyd, Owen Casciotti
# Github Link    : https://github.com/michealcarac/VSLAM-Mapping
# Description    : A* For Occupancy Grid Map
# Original Author: Nicholas Swift
# Article on code: https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
# ------------------------------------------------------------------------------


import numpy as np
import heapq
import matplotlib.pyplot as plt
from matplotlib import colors

from OccupancyGridMap import OccupancyGridMap
from MapFileUnpacker import Unpacker

class NodeStar:
    def __init__(self,parent=None,position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position} - g:{self.g} h:{self.h} f:{self.f}"

    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f

def return_path(current_node):
    path = []
    current = current_node
    i = 0
    while current is not None:
        path.append(current.position)
        current = current.parent
    path = path[::-1]

    for i in range(len(path)-1):
        pos = path[i]
        next_pos = path[i+1]
        if next_pos[1]-pos[1] == 0:
            if next_pos[0] > pos[0]:
                angle = 90
            else:
                angle = 270
        else:
            if next_pos[1] > pos[1]:
                angle = 0
            else:
                angle = 180
        path[i] = [pos[0],pos[1],angle]
    path[-1] = [path[-1][0],path[-1][1],path[-2][2]]
    return path# Reversed path

def astar(map,start,end):
    # Create start and end nodes
    start_node = NodeStar(None, start)
    start_node.g = start_node.h = start_node.f = 0

    end_node = NodeStar(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Defined empty open and closed lists
    open_list = []
    closed_list = []

    # Heapify open_list and add the start_node
    heapq.heapify(open_list)
    heapq.heappush(open_list,start_node)

    # Adding a stop condition
    out_i = 0
    max_i = map.getMaxCol()*map.getMaxRow()

    # Squares we search for
    near_squares = ((0,-1),(0,1),(-1,0),(1,0))   # Four Directions, up,down,left,right

    while len(open_list) != 0:  # While open list is not empty

        out_i += 1
        if out_i > max_i:
            # If we hit this point, it technically did not find a path so
            # Return the path
            print("Inefficient Path")
            return return_path(current_node)

        # Grab current node off of the heap
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # If goal is found, return the path
        if current_node == end_node:
            return return_path(current_node)

        # Children!
        children = []

        for neighbor in near_squares:
            new_pos = (current_node.position[0] + neighbor[0], current_node.position[1] + neighbor[1])
            if map.isValidIndexPoint(new_pos[::-1]): #Function takes in as X,Y, so we flip from Y,X
                if map.isUnoccupiedIndex(new_pos[::-1]): #Function takes in as X,Y
                    new_node = NodeStar(current_node, new_pos)
                    if not (new_node in open_list):
                        children.append(new_node)

        for child in children:
            # Child on closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue

            # Create Heuristic
            #child.g = current_node.g + 1
            #child.g = abs(child.position[0] - start_node.position[0]) + abs(child.position[1] - start_node.position[1])
            child.g = current_node.g
            #child.g = current_node.g + abs(child.position[0] - start_node.position[0]) + abs(child.position[1] - start_node.position[1])
            # Manhattan Distance
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1])

            child.f = child.g + child.h
            # Child on open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                continue

            # Add child to open list
            heapq.heappush(open_list,child)

    return None

if __name__ == "__main__":
    ogm = OccupancyGridMap()

    # Get keyframe data from map file
    print("Unpacking MSG file...")
    unpack = Unpacker("../data/map.msg")
    keyframes = unpack.extract_keyframe_data()
    # Remove z axis data
    keyframes = np.delete(keyframes, 2, 1)

    # Create mapdata
    print("Loading map data...")
    ogm.fromMapMSGData(keyframes)
    # ogm.fromCSV("Map.csv")
    # ogm.fromKeyframesCSV("../data/keyframes.csv")

    print(ogm.grid_map)
    start = (1,0)
    #     row^ ^column
    end =(20,7)
    #   row^ ^column
    line = astar(ogm,start,end)
    print(line)

    # FROM VISUALIZE MAP # CDL=> Removed for now
    # cmap = colors.ListedColormap(['brown', 'blue', 'green', 'brown'])
    # bounds = [-1000, 0, ogm.cell_threshold, 1, 1000]
    # norm = colors.BoundaryNorm(bounds, cmap.N)
    # fig, ax = plt.subplots()
    # ax.imshow(ogm.grid_map, origin='lower', cmap=cmap, norm=norm)
    # When doing poorly formatted maps:
    #ax.imshow(ogm.grid_map, origin='lower', cmap=cmap, norm=norm, aspect='auto')

    # Visualize gridmap
    fig, ax = ogm.visualizeGrid()

    # Add A star path points to map
    markersize = 100 # Size of start and end points (5-100 is a good range)
    if line != None:
        for point in line:
            ax.scatter(point[1], point[0])

    ax.scatter(start[1],start[0],s=markersize)
    ax.scatter(end[1],end[0],s=markersize)
    fig.show()



