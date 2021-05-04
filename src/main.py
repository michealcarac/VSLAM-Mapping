import numpy as np
from AStarOCC import astar
from OccupancyGridMap import OccupancyGridMap
from MapFileUnpacker import Unpacker
from send_location import send_live_location
# from JetsonMotorInterface import *
import time

unpacker = Unpacker()
occ_map = OccupancyGridMap()
map_file = '../data/map.msg'
sleep_time_forward = 1
sleep_time_turn = 1

# Steps

# 1. Extract Keyframes
# Python file
unpacker.unpackMSGmap(map_file)
keyframes = unpacker.extract_keyframe_data()
# p = np.deg2rad(12.5)
# for i in range(len(keyframes)):
#     keyframes[i][0] = keyframes[i][0] * np.cos(p) - keyframes[i][1] * np.sin(p)
#     keyframes[i][1] = keyframes[i][0] * np.sin(p) + keyframes[i][1] * np.cos(p)
#     keyframes[i][2] = keyframes[i][2]

# Remove z axis data
keyframes = np.delete(keyframes, 2, 1)

# 2. Generate OCC Map
# Python file
occ_map.fromMapMSGData(keyframes)

# 4. Find start on OCC
# Python File
start = (0, 1)  # Col, Row (x, y)


# 5. Send OCC + start to android
# Python File
# Uncomment when On jetson
# occ_map.numpyArrayToCSV("/var/www/html/occupancy_map_data.csv")
# send_live_location(start)

def main(end = None)

    # 6. Get end location from android
    if end == None:
        end = (7, 20)

    #7. Run A* and save path
    path = astar(occ_map, start, end)

    # 8. Follow A* path and send to android
        # Python File
    # initPins()
    print('Starting')
    for i in range(len(path)-1):
        pos1 = path[i]
        pos2 = path[i+1]
        print(i, pos1, pos2)
        send_live_location(pos2)
        # Move Forward
        if pos2[0] != pos1[0] or pos2[1] != pos1[1]:
            # Call motor move forward
            # goForwards()
            print('Forward')
            time.sleep(sleep_time_forward)

        if pos1[2] == pos2[2]:
            pass
        elif pos1[2] < pos2[2]:
            # Call motor turn left
            # goLeft()
            print('Left')
            time.sleep(sleep_time_turn)

        elif pos1[2] > pos2[2]:
            # Call motor turn right
            # goRight()
            print('Right')
            time.sleep(sleep_time_turn)


