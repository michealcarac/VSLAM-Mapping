# ------------------------------------------------------------------------------
# Name         : OccupancyGridMap.py
# Date Created : 2/22/2021
# Author(s)    : Micheal Caracciolo, Chris Lloyd, Owen Casciotti
# Github Link  : https://github.com/michealcarac/VSLAM-Mapping
# Description  : A simple occupancy grid map.
# ------------------------------------------------------------------------------

# Internal Imports
from MapFileUnpacker import * # For test purposes

# External Imports
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np
import csv
from typing import Tuple

class OccupancyGridMap:
    """
    A class to implement a simple occupancy grid map.

    The occupancy grid is defined as a matrix of values. These values
    represent the likelyhood that a grid cell is occupied or not.

    Values between (0 - 1) indicate the value of occupancy. Within that
    range, whether a cell is considered occupied, is dependant on a whether
    it is greater than a certain threshold (cell_threshold).
    If these values are out of a specific range, or specifically -1, they are
    considered unknown or unvisited.

    A cell is occupied if its value >= occupancy_threshold.

    Each cell represents a physical square of area with a specified size:

    length = width = (cell_size)

    This allows to go between coordinates and actual position.

    Attributes:
        grid_map (matrix of float32): The occupancy grid map cell data.
        cell_threshold (float32):     The threshold to determine if a cell is
                                                                    occupied or not.
        cell_size (float32):          The unitless size that a single cell
                                                                    (width and height) represents.
        trans_pt (Tuple point):       A point to shift the gridmap by.
    """

    def __init__(self, _grid_map=[], _cell_threshold=0.5, _cell_size=1, _trans_pt = (0,0)):
        """
        The default constructor for class OccupancyGridMap.

        Args:
            _grid_map (matrix of float32): A datamap to use as the gridmap.
            _cell_threshold (float32):     The threshold for a cell being occupied
            _cell_size (float32):          The unitless size of a cell's length and width.
            _trans_pt (Tuple point):       A point to shift the gridmap by.
        """

        self.grid_map       = _grid_map
        self.cell_threshold = _cell_threshold
        self.cell_size      = _cell_size
        self.trans_pt       = _trans_pt

    # ----------------------------------------------------------------------------
    # Class Methods
    # ----------------------------------------------------------------------------

    def getDataIndex(self, index_point):
        """
        Method to get the occupancy value at a certain index location.

        Args:
            index_point (tuple of int): An indexed point (x, y).

        Returns:
            value (float32): The value of occupancy.
        """

        # Ensure the point is valid
        if (not self.isValidIndexPoint(index_point)):
            print("ERROR: Entered point is invalid!")
            return -1 # CDL=> Replace with exception later

        # Get index point x,y
        x, y = index_point

        # Get the value of occupancy
        return self.grid_map[y][x]

    def setDataIndex(self, index_point, value):
        """
        Method to set the occupancy value at a certain index location.

        Args:
            index_point (tuple of int): An indexed point (x, y).
            value (float32):            The value of occupancy to set.

        Returns:
            value (float32): The value of occupancy.
        """

        # Ensure the point is valid
        if (not self.isValidIndexPoint(index_point)):
            print("ERROR: Entered point is invalid!")
            return -1 # CDL=> Replace with exception later

        # Get index point x,y
        x, y = index_point

        # Set the occupancy value
        self.grid_map[y][x] = value

        return value

    def isOccupiedIndex(self, index_point):
        """
        Method to check if index point is occupied.

        Args:
            index_point (tuple of int): An indexed point (x, y).

        Returns:
            status (bool): Whether the position is occupied.
        """

        # Ensure the point is valid
        if (not self.isValidIndexPoint(index_point)):
            print("ERROR: Entered point is invalid!")
            return -1 # CDL=> Replace with exception later

        # Get index point x,y
        x, y = index_point

        # Get the occupancy value
        value = self.grid_map[y][x]

        # Get occupied status
        return (self.cell_threshold <= value <= 1)

    def isUnoccupiedIndex(self, index_point):
        """
        Method to check if index point is unoccupied.

        Args:
            index_point (tuple of int): An indexed point (x, y).

        Returns:
            status (bool): Whether the position is unoccupied.
        """

        # Ensure the point is valid
        if (not self.isValidIndexPoint(index_point)):
            print("ERROR: Entered point is invalid!")
            return -1 # CDL=> Replace with exception later

        # Get index point x,y
        x, y = index_point

        # Get the occupancy value
        value = self.grid_map[y][x]

        # Get occupied status
        return (0 <= value <= self.cell_threshold)

    def isUnknownIndex(self, index_point):
        """
        Method to check if index point is unknown.

        Args:
            index_point (tuple of int): An indexed point (x, y).

        Returns:
            status (bool): Whether the position is unknown.
        """

        # If not occupied or unoccupied, then unknown
        return not (self.isOccupiedIndex(index_point) or self.isUnoccupiedIndex(index_point))

    def isValidIndexPoint(self, index_point):
        """
        Method to check if index point is valid.

        Args:
            index_point (tuple of int): An indexed point (x, y).

        Returns:
            status (bool): Whether the position is valid.
        """

        # Get index point x,y
        x, y = index_point

        # Ensure the point is valid
        return ((0 <= x < len(self.grid_map[0])) and
                (0 <= y < len(self.grid_map)))

    def getMaxRow(self):
        """
        Method to get the max row (y value).

        Returns:
            numRows (int): The max row value.
        """
        return len(self.grid_map)

    def getMaxCol(self):
        """
        Method to get the max col (x value).

        Returns:
            numCols (int): The max col value.
        """
        return len(self.grid_map[0])

    def getMaxPoint(self):
        """
        Method to get the max point (x,y).

        Returns:
            maxPoint (int,int): The max index point as a tuple.
        """
        return (self.getMaxCol(), self.getMaxRow())

    def locToIndex(self, loc_point):
        """
        Method to convert a coordinate point to an index point.

        Args:
            loc_point (tuple of float32): A real world point (x, y). Scaled by cell_threshold.

        Returns:
            index_point (tuple of int): An indexed point (x, y).
        """
        scaledPt = list(int(round(axis / self.cell_size)) for axis in loc_point)
        return (scaledPt[0] - self.trans_pt[0], scaledPt[1] - self.trans_pt[1])

    def indexToLoc(self, index_point):
        """
        Method to check if index point is valid.

        Args:
            index_point (tuple of int): An indexed point (x, y).

        Returns:
            loc_point (tuple of float32): A real world point (x, y). Scaled by cell_threshold.
        """
        translatedPt = (index_point[0] + self.trans_pt[0], index_point[1] + self.trans_pt[1])
        return list((axis * self.cell_size) for axis in translatedPt)

    def getRealLocations(self,path):
        """
        Converts the index path to a real world coord path
        Args:
            path: Index Path of type List

        Returns:

        """
        line = []
        for coord in path:
            x = coord[0]
            y = coord[1]
            theta = coord[2]
            point = self.indexToLoc([x, y])
            line.append([point[0], point[1], theta])

        return line

    def ICP(self,fixed,variable):
        """
        Method to run Iterative Closest Point Algorithm
        Args:
            fixed: Fixed Path (Control path) in real world coords
            variable: Path that is fitted to Fixed Path in real world coords

        Returns:
            path: The Adjusted Path
        """
        print(fixed)
        print(variable)
        indices = []
        dist_2 = []
        nodes = np.asarray(fixed)
        #for node in variable:
        #    nodes = np.asarray(nodes)
        #    nodexy = [node[0],node[1]]
        #    print(node[2])
        #    if node[2] == 90 or node[2] == 270:
        #        print(node)
        #        dist_2 = np.sum((nodes - [0,nodexy[1]])**2, axis=1)
        #        print(dist_2)
        #        indices.append(np.argmin(dist_2))
        #    elif node[2] == 0 or node[2] == 180:
        #        print(node)
        #        dist_2 = np.sum((nodes - [nodexy[0],0])**2, axis=1)
        #        print(dist_2)
        #        indices.append(np.argmin(dist_2))
        for index,node in enumerate(variable):  # To check every variable Point
            if node[2] == 90 or node[2] == 270: # If going Vertical
                for i in range(len(nodes)):     # To check for every fixed Point to every variable
                    if nodes[i,1] - node[1] <= 0 and nodes[i,1] - node[1] >= -.2: #Must slightly be below variable point
                        #print("value:", nodes[i,0],nodes[i,1],"difference:",nodes[i,1]-node[1])
                        #print((nodes[i,0] - node[0])**2)
                        #print(index)
                        if abs((nodes[i,0]-node[0])) <1: # Tolerance for X values
                            dist_2.append(abs((nodes[i,0] - node[0])**2)) #Append distance in X values to distance array
                    else:
                        dist_2.append(100000) # For garbage distances
                    print(dist_2)

                indices.append(np.argmin(dist_2)) # Append min distance index to indices array
                dist_2 = [] # Resets distance array

            elif node[2] == 0 or node[2] == 180: # If going Horizontal (TODO: THIS ONE NEEDS TO BE ADJUSTED)
                for i in range(len(nodes)):
                    if nodes[i,0] - node[0] <= 0 and nodes[i,0] - node[0] >= -.4: #Must slightly be right of variable pt (maybe?)
                        if abs((nodes[i,1] - node[1])) < 1: # Tolerance for Y values
                            dist_2.append(abs((nodes[i,1] - node[1])**2)) #Append distance in Y values to distance array
                    else:
                        dist_2.append(100000) # For garbage distances
                indices.append(np.argmin(dist_2)) # Append min distance index to indices array
                dist_2 = [] # Resets distance array



        #for node in variable:
        #    nodexy = [node[0],node[1]]
        #    nodes = np.asarray(nodes)
        #    print("difference:", (nodes-nodexy)**2)
        #    dist_2 = np.sum((nodes - nodexy) ** 2, axis=1)
        #    print(dist_2)
        #    indices.append(np.argmin(dist_2))
        print(indices)
        return indices

    def visualizeGrid(self):
        """
        Method to visualize a map of data.

        Args: None # CDL=> Add any config settings?
        # Add setting to plot occ/unocc/unknown OR heatmap?

        Returns: None
        """

        # Create discrete colormap
        # Brown : Unknown
        # Blue  : Unoccupied
        # Green : Occupied
        cmap = colors.ListedColormap(['brown', 'blue', 'green', 'brown'])
        bounds = [-1000, 0, self.cell_threshold, 1, 1000]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        # CDL=> Add title? Option to enable axis?
        fig, ax = plt.subplots()
        ax.imshow(self.grid_map, origin='lower', cmap=cmap, norm=norm)

        plt.axis("off")
        plt.show()
        return fig, ax

    def numpyArrayToCSV(self):
        """
        Method to make a csv file of occupancy grid map data from numpy array.

        """
        # save array into csv file
        np.savetxt("/var/www/html/occupancy_map_data.csv", self.grid_map,
                  delimiter=",")


    def fromCSV(self, filename):
        """
        Method to import a gridmap from a csv file.

        Note: This method overwrites current grid map!

        Args:
            filename (string): The file containing MxN csv data.

        Returns: None
        """ # CDL=> Not needed. Remove later
        with open(filename, 'r') as fd:
            reader = csv.reader(fd)
            self.grid_map = np.array(list(reader)).astype("float")

    def fromKeyframesCSV(self, filename):
        """
        Method to import a gridmap from a csv file of keyframe points.

        Note: This method overwrites current grid map!

        Args:
            filename (string): The file containing csv point data.
        """

        # Import the keyframe data
        keyframes = np.genfromtxt(filename, delimiter=",")

        # Create the gridmap
        self.fromMapMSGData(keyframes)

    def fromMapMSGData(self, keyframes):
        """
        Method to import a gridmap from a array of keyframe points.

        Note: This method overwrites current grid map!

        Args:
            keyframes (array of float32 points): The keyframe point data.
        """
        # Calculate scale factor for data
        # Keep increasing scale by factor until every gridmap is valid
        # I.E: It satisfies the following two conditions:
        # 1.) Every unoccupied grid tile has an adjacent edge
        # 2.) If an unoccupied grid tile has an unoccupied corner tile, there
        #     is an adjacent unoccupied tile to both the current tile and the
        #     corner tile of interest.
        scale_adjustment = 0.1
        scale = 0
        notdone = True
        while notdone: # While the gridmap is not valid
            scale += scale_adjustment
            scaledKeyframes = keyframes / scale

            # Save the scale for further use
            self.cell_size = scale

            # Find the max point to allocate gridmap
            max_point = np.ceil(np.amax(scaledKeyframes, axis=0)).astype(int)
            # Allocate array to max point size
            self.grid_map = np.full(max_point, 0.6).transpose()

            # Translate array of points to positive numbers
            # Calculate minimum point
            minValueX = np.amin(scaledKeyframes[:, 0])
            minValueY = np.amin(scaledKeyframes[:, 1])

            # Only translate dimension if smallest point is negative
            if (minValueX < 0):
                scaledKeyframes[:, 0] -= minValueX
            if (minValueY < 0):
                scaledKeyframes[:, 1] -= minValueY

            # Save the translation point for further use
            self.trans_pt = (minValueX, minValueY)

            # Set keyframe nearest integer point to 0 (unoccupied)
            for point in scaledKeyframes:
                x_index = int(np.floor(point[0]))
                y_index = int(np.floor(point[1]))
                self.setDataIndex((x_index, y_index), 0)

            # Check if gridmap is valid
            notdone = not self.isMapValid()

    def isMapValid(self):
        """
        Method to ensure gridmap is valid.

        A gridmap is valid iff all unoccupied tiles have an adjacent square that
        is also unoccupied and if there are any corner points that are
        unoccupied then a adjacent edge to that corner and the current tile,
        which is unoccupied exists.

        Returns:
            valid (bool): Whether or not the gridmap is valid.
        """
        for y in range(len(self.grid_map)):
            for x in range(len(self.grid_map[0])):
                if self.isUnoccupiedIndex((x,y)):
                    currPt = (x,y)
                    adjacentEdgePts =   [(0,-1),(0,1),(-1,0),(1,0)]
                    diagonalCornerPts = [(1,1), (1,-1), (-1,1), (-1,-1)]

                    # Check to see if there are any corners with an adjacent edge
                    for cornerPt in diagonalCornerPts:
                        edge1Pt = (currPt[0] + cornerPt[0], currPt[1])
                        edge2Pt = (currPt[0], currPt[1] + cornerPt[1])
                        cornerPt = (currPt[0] + cornerPt[0], currPt[1] + cornerPt[1])

                        if self.isValidIndexPoint(cornerPt) and self.isUnoccupiedIndex(cornerPt):
                            if not ((self.isValidIndexPoint(edge1Pt) and self.isUnoccupiedIndex(edge1Pt)) or
                                    (self.isValidIndexPoint(edge2Pt) and self.isUnoccupiedIndex(edge2Pt))):
                                return False

                    # Check to see if there are any adjacent edges
                    validEdge = False
                    for edgePt in adjacentEdgePts:
                        adjacentPt = (currPt[0] + edgePt[0], currPt[1] + edgePt[1])
                        if self.isValidIndexPoint(adjacentPt) and self.isUnoccupiedIndex(adjacentPt):
                            validEdge = True
                    if not validEdge:
                        return False
        return True

# ------------------------------------------------------------------------------
# End of class OccupancyGridMap
# ------------------------------------------------------------------------------

# Main code for this file. Only runs if this file is the top file
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
    #ogm.fromCSV("Map.csv")
    #ogm.fromKeyframesCSV("../data/keyframes.csv")

    print("Visualizing grid map data...")
    ogm.visualizeGrid()

    # Calculate the location (camera coordinates) of an index point
    print("(0,1): ", ogm.indexToLoc((0,1)))
