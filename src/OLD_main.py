# ------------------------------------------------------------------------------
# Name         : OLD_main.py
# Date Created : 2/22/2021
# Author(s)    : Micheal Caracciolo, Chris Lloyd, Owen Casciotti
# Github Link  : https://github.com/michealcarac/VSLAM-Mapping
# Description  : A testing main, no motor control
# ----------------------------------------------

import numpy as np
import matplotlib.pyplot as plt

# Import our custom modules
from AStarOCC import astar
from OccupancyGridMap import OccupancyGridMap
from MapFileUnpacker import Unpacker

if __name__ == "__main__":
    # Initialize Objects
    ogm = OccupancyGridMap()
    unpack = Unpacker()

    # Get keyframe data from map file (.msg)
    print("Unpacking MSG file...")
    unpack.unpackMSGmap("../data/ECELAB_V3_map.msg")
    keyframes = unpack.extract_keyframe_data()

    t = 1  # Set 1 if need rotation
    p = np.deg2rad(-10)  # Rotation value
    if t == 1:
        # Rotate around z
        for i in range(len(keyframes)):
            keyframes[i][0] = keyframes[i][0] * np.cos(p) - keyframes[i][1] * np.sin(p)
            keyframes[i][1] = keyframes[i][0] * np.sin(p) + keyframes[i][1] * np.cos(p)
            keyframes[i][2] = keyframes[i][2]

    # Remove z axis data
    keyframes = np.delete(keyframes, 2, 1)

    # Create mapdata
    print("Loading map data...")
    ogm.fromMapMSGData(keyframes)
    # ogm.fromCSV("../data/Map.csv")
    # ogm.fromKeyframesCSV("../data/keyframes.csv")

    print(ogm.grid_map)
    start = (8, 19)
    #       x^ ^y
    end = (0, 0)
    #    x^ ^y
    line = astar(ogm, start, end)
    print(line)

    # Visualize gridmap
    fig, ax = ogm.visualizeGrid()

    # Add A star path points to map
    markersize = 100  # Size of start and end points (5-100 is a good range)
    if line is not None:
        for point in line:
            ax.scatter(point[0], point[1])

    ax.scatter(start[0], start[1], s=markersize)
    ax.scatter(end[0], end[1], s=markersize)
    plt.savefig('../images/OLD_main.png')
    plt.show()
