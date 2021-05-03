import numpy as np
from AStarOCC import astar
from OccupancyGridMap import OccupancyGridMap
from MapFileUnpacker import Unpacker
from send_location import send_live_location

unpacker = Unpacker()
occ_map = OccupancyGridMap()
map_file = '../../ECELAB_V2_map.msg'

# Steps

# 1. Extract Keyframes
    # Python file
unpacker.unpackMSGmap(map_file)
keyframes = unpacker.extract_keyframe_data()
p = np.deg2rad(12.5)
for i in range(len(keyframes)):
    keyframes[i][0] = keyframes[i][0] * np.cos(p) - keyframes[i][1] * np.sin(p)
    keyframes[i][1] = keyframes[i][0] * np.sin(p) + keyframes[i][1] * np.cos(p)
    keyframes[i][2] = keyframes[i][2]

# Remove z axis data
keyframes = np.delete(keyframes, 2, 1)

# 2. Generate OCC Map
    # Python file
occ_map.fromMapMSGData(keyframes)

# 3. Use VSLAM Localization
    # C File
local_point = [0,0]

# 4. Find start on OCC
    # Python File

#start = occ_map.locToIndex(local_point)
start = [5,4] #Test Variable

# 5. Send OCC + start to android
    # Python File
    # Only first loop

#Uncomment when On jetson
#occ_map.numpyArrayToCSV()
#send_live_location(start)

# 8. Follow A* path and send to android
    # Python File
path = None # read from path.csv
pos1 = path[0]
pos2 = path[1]
# Move Forward
curr = occ_map.locToIndex(local_point)
while curr[0] != pos1[0] and curr[1] != pos1[1]:
    # Call motor move forward
    pass
if pos1[2] == pos2[2]:
    pass
elif pos1[2] < pos2[2]:
    pass
    # Call motor turn left
elif pos1[2] > pos2[2]:
    pass
    # Call motor turn right

# 9. Repeat back to 3, skip 5 and 6
    # Python File

