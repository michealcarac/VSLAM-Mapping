import websockets
import csv, json

# uri = "ws://localhost:9001"
uri = "ws://128.153.161.14:9001"


async def send_live_location(pos):
    x,y = pos
    async with websockets.connect(uri) as websocket:
        json_data = {"data_type": "position", "x": x, "y": y}
        json_data = json.dumps(json_data, indent=4)
        await websocket.send(json_data)
        print("Data Sent" + json_data)

