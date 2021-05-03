import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import rotate

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
    unpack.unpackMSGmap("../../ECELAB_V2_map.msg")
    keyframes = unpack.extract_keyframe_data()

    p = np.deg2rad(12.5) #Rotation value
    #rotate around x
    #for i in range(len(keyframes)):
    #    keyframes[i][0] = keyframes[i][0]
    #    keyframes[i][1] = keyframes[i][1] * np.cos(p) - keyframes[i][2] * np.sin(p)
    #    keyframes[i][2] = keyframes[i][1] * np.sin(p) + keyframes[i][2] * np.cos(p)
    #rotate around y
    #for i in range(len(keyframes)):
    #    keyframes[i][0] = keyframes[i][0] * np.cos(p) + keyframes[i][2] * np.sin(p)
    #    keyframes[i][1] = keyframes[i][1]
    #    keyframes[i][2] = keyframes[i][2] * np.cos(p) - keyframes[i][0] * np.sin(p)
#
    #Rotate around z
    for i in range(len(keyframes)):
        keyframes[i][0] = keyframes[i][0] * np.cos(p) - keyframes[i][1] * np.sin(p)
        keyframes[i][1] = keyframes[i][0] * np.sin(p) + keyframes[i][1] * np.cos(p)
        keyframes[i][2] = keyframes[i][2]

    # Remove z axis data
    keyframes = np.delete(keyframes, 2, 1)

    # Create mapdata
    print("Loading map data...")
    ogm.fromMapMSGData(keyframes)
    # ogm.fromCSV("Map.csv")
    # ogm.fromKeyframesCSV("../data/keyframes.csv")

    print(ogm.grid_map)
    start = (2,4)
    #     row^ ^column
    end =(1,7)
    #   row^ ^column
    line = astar(ogm,start,end)
    print(line)
#

    # Visualize gridmap
    fig, ax = ogm.visualizeGrid()
#
    # Add A star path points to map
    markersize = 100 # Size of start and end points (5-100 is a good range)
    if line != None:
        for point in line:
            ax.scatter(point[0], point[1])

    ax.scatter(start[1],start[0],s=markersize)
    ax.scatter(end[1],end[0],s=markersize)
    fig.show()
#
    Realline = ogm.getRealLocations(line)

    Reallinexy = [] #realline without angle {temp until I can feed in the angle to ICP}
    keyframesxy = []
    plt.figure()
    for point in Realline:
        plt.scatter(point[0],point[1])
        Reallinexy.append([point[0],point[1]])
    for point in keyframes:
        plt.scatter(point[0], point[1], c='#1f77b4')
        keyframesxy.append([point[0],point[1]])
    plt.show()
    print(keyframes)

