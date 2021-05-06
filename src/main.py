# ------------------------------------------------------------------------------
# Name         : main.py
# Date Created : 5/01/2021
# Author(s)    : Micheal Caracciolo, Owen Casciotti, Chris Lloyd
# Github Link  : https://github.com/michealcarac/VSLAM-Mapping
# Description  : Main program to run everything. Only to be ran on Jetson, otherwise try OLD_main.py
# ------------------------------------------------------------------------------


import numpy as np
import time

from AStarOCC import astar
from OccupancyGridMap import OccupancyGridMap
from MapFileUnpacker import Unpacker
from send_location import send_live_location
from JetsonMotorInterface import *

initPins()

unpacker = Unpacker()
occ_map = OccupancyGridMap()
# map_file = '../data/map.msg'
map_file = '../../ECELAB_V3_map.msg'

# Steps

# 1. Extract Keyframes
unpacker.unpackMSGmap(map_file)
keyframes = unpacker.extract_keyframe_data()

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

# 2. Generate OCC Map
occ_map.fromMapMSGData(keyframes)

# 4. Find start on OCC
# Ideal: To find current localized point in real time
start = (0, 12)  # Col, Row (x, y)


# 5. Send OCC + start to android
# Uncomment when On jetson/Phone set up
# occ_map.numpyArrayToCSV("/var/www/html/occupancy_map_data.csv") #For phone to grab
# send_live_location(start)

def main(end=None):
    # 6. Get end location from android
    if end is None:
        end = (6, 19)  # Col, Row (x,y)

    # 7. Run A* and save path
    path = astar(occ_map, start, end)
    print(path)

    # Visualize gridmap
    fig, ax = occ_map.visualizeGrid()

    # Add A star path points to map
    markersize = 100  # Size of start and end points (5-100 is a good range)
    if path is not None:
        for point in path:
            ax.scatter(point[0], point[1])

    ax.scatter(start[0], start[1], s=markersize)
    ax.scatter(end[0], end[1], s=markersize)
    fig.savefig('../images/mainMap.png')

    # 8. Follow A* path and send to android
    # Python File
    print('Starting')
    for j in range(len(path) - 1):
        # Explanation: These Y values and sleep values were measured in real time, Not needed if running with
        # localization, however, we are not using localization as OPEN-VSLAM is now a terminated program.
        if path[j][1] <= 19 & path[j][1] >= 12:  # Check Y Value
            sleep_time_forward = 1.4  # Change these values according to speed
            sleep_time_turn = 4.2  # Change these values according to speed
            print('Going Speed 1')
        elif path[j][1] >= 0 & path[j][1] < 12:  # Check Y Value
            sleep_time_forward = 2.44  # Change these values according to speed
            sleep_time_turn = 4.2  # Change these values according to speed
            print('Going Speed 2')

        pos1 = path[j]
        pos2 = path[j + 1]
        print(j, pos1, pos2)
        # send_live_location(pos2)
        # Move Forward
        if pos2[0] != pos1[0] or pos2[1] != pos1[1]:
            # Call motor move forward
            stopMotors()
            goForwards()
            print('Forward')
            time.sleep(sleep_time_forward)

        if pos1[2] == pos2[2]:
            pass
        elif pos1[2] < pos2[2]:
            # Call motor turn left
            stopMotors()
            goLeft()
            print('Left')
            time.sleep(sleep_time_turn)

        elif pos1[2] > pos2[2]:
            # Call motor turn right
            stopMotors()
            goRight()
            print('Right')
            time.sleep(sleep_time_turn)
    stopMotors()


main()  # TO BE replaced with a send location to phone and call main with a end value
