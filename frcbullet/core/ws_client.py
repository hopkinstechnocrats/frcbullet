import asyncio
import json
import websockets


class WSInterface:

    def __init__(self, num_joints: int):
        self.num_joints = num_joints
        self.joint_commands = [0] * num_joints

    def get_joint_commands(self):
        return self.joint_commands

    async def set_joint_commands(self):
        uri = "ws://localhost:3300/wpilibws"
        while True:
            try:
                async with websockets.connect(uri) as websocket:
                    while True:
                        response_json = await websocket.recv()
                        response = json.loads(response_json)
                        if response["type"] == "PWM":
                            if response["device"] in map(lambda x: str(x), range(self.num_joints)):
                                if "<speed" in response["data"].keys():
                                    self.joint_commands[int(response["device"])] = response["data"]["<speed"]
            except:
                pass