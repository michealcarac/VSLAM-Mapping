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
    unpack.unpackMSGmap("../../../ECELAB_map.msg")
    keyframes = unpack.extract_keyframe_data()

    p = np.deg2rad(13) #Rotation value
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

    #print(ogm.grid_map)
    #start = (0,0)
    ##     row^ ^column
    #end =(20,7)
    ##   row^ ^column
    #line = astar(ogm,start,end)
    #print(line)
#
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
#
    ## Add A star path points to map
    #markersize = 100 # Size of start and end points (5-100 is a good range)
    #if line != None:
    #    for point in line:
    #        ax.scatter(point[0], point[1])
#
    #ax.scatter(start[1],start[0],s=markersize)
    #ax.scatter(end[1],end[0],s=markersize)
    fig.show()
#
    #Realline = ogm.getRealLocations(line)
#
    #Reallinexy = [] #realline without angle {temp until I can feed in the angle to ICP}
    #keyframesxy = []
    #plt.figure()
    #for point in Realline:
    #    plt.scatter(point[0],point[1])
    #    Reallinexy.append([point[0],point[1]])
    #for point in keyframes:
    #    plt.scatter(point[0], point[1], c='#1f77b4')
    #    keyframesxy.append([point[0],point[1]])
    #plt.show()
    #print(keyframes)
#
    ## Plots lines between points
    #for i in range(len(keyframes)-1):
    #    deltax = keyframes[i][0] - keyframes[i+1][0]
    #    deltay = keyframes[i][1] - keyframes[i+1][1]
    #    if abs(deltax) <= 2 and abs(deltay) <= 2:
    #        x_values = [keyframes[i][0],keyframes[i+1][0]]
    #        y_values = [keyframes[i][1], keyframes[i+1][1]]
    #        plt.plot(x_values,y_values)
    #plt.show()
#
    ## TODO: MESSING WITH ICP
    #xyangle_path = ogm.ICP(keyframesxy, Realline,1)
    #path = []
    #for point in Realline:
    #    plt.scatter(point[0],point[1])
    #    Reallinexy.append([point[0],point[1]])
    #for point in keyframes:
    #    plt.scatter(point[0], point[1], c='#1f77b4')
    #    keyframesxy.append([point[0],point[1]])
    #for i in range(len(xyangle_path)):
    #    x_values = xyangle_path[i][0]
    #    y_values = xyangle_path[i][1]
    #    angle = xyangle_path[i][2]
    #    print(xyangle_path[i])
    #    path.append([x_values,y_values])
    #    #time.sleep(.5)
    #    #for i in range(len(keyframesxy)):
    #        #print(keyframesxy[i][0])
    #    #    plt.scatter(keyframesxy[i][0],keyframesxy[i][1],c='#1f77b4')
    #    plt.scatter(x_values,y_values,c='#ff7f0e')
    #plt.show()
    #print(path)
#
    #ogm.plotKeyframes("../data/keyframesorb.csv",' ')
    for point in keyframes:
        plt.scatter(point[0], point[1], c='#1f77b4')
    plt.show()
