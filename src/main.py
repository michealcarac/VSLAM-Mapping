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
    unpack.unpackMSGmap("../data/map.msg")
    keyframes = unpack.extract_keyframe_data()
    # Remove z axis data
    keyframes = np.delete(keyframes, 2, 1)

    # Create mapdata
    print("Loading map data...")
    ogm.fromMapMSGData(keyframes)
    # ogm.fromCSV("Map.csv")
    # ogm.fromKeyframesCSV("../data/keyframes.csv")

    print(ogm.grid_map)
    start = (0,0)
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
            ax.scatter(point[0], point[1])

    ax.scatter(start[1],start[0],s=markersize)
    ax.scatter(end[1],end[0],s=markersize)
    fig.show()

    Realline = ogm.getRealLocations(line)


    plt.figure()
    plt.scatter(keyframes[:, 0], keyframes[:, 1])
    for point in Realline:
        plt.scatter(point[0],point[1])
    plt.show()
    print(keyframes)
    for i in range(len(keyframes)-1):
        deltax = keyframes[i][0] - keyframes[i+1][0]
        deltay = keyframes[i][1] - keyframes[i+1][1]
        if abs(deltax) <= 2 and abs(deltay) <= 2:
            x_values = [keyframes[i][0],keyframes[i+1][0]]
            y_values = [keyframes[i][1], keyframes[i+1][1]]
            plt.plot(x_values,y_values)
    print(Realline)
    plt.show()
