# ------------------------------------------------------------------------------
# Name         : MapFileUnpacker.py
# Date Created : 2/22/2021
# Author(s)    : Kyle Bielby
# Github Link  : https://github.com/michealcarac/VSLAM-Mapping
# Description  : Foundation to send path/map/position to Phone
# ------------------------------------------------------------------------------

import json
import csv
import websockets

# uri = "ws://localhost:9001"
uri = "ws://128.153.161.14:9001"  # Placeholder url.


# Still need to add more sends
async def send_live_location(pos):
    x, y = pos
    async with websockets.connect(uri) as websocket:
        json_data = {"data_type": "position", "x": x, "y": y}
        json_data = json.dumps(json_data, indent=4)
        await websocket.send(json_data)
        print("Data Sent" + json_data)
