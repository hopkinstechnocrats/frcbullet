import asyncio
import json
import re
import logging

import websockets


class WSInterface:

    def __init__(self, num_joints: int):
        self.num_joints = num_joints
        self.joint_commands = [0] * num_joints
        self.uri = "ws://localhost:3300/wpilibws"
        self.joint_states = [(0.0, 0.0)] * num_joints

    def get_joint_commands(self):
        return self.joint_commands

    def set_joint_states(self, joint_states):
        self.joint_states = [(x[0], x[1]) for x in joint_states]

    def parse_responses(self, response):
        logging.debug("response received from server")
        if response["type"] == "SimDevice":
            logging.info("simDevice updated")
            if response["device"] in map(lambda x: "VelocityJointMotor[" + str(x) + "]", range(self.num_joints)):
                logging.warning("specific simDevice updated")
                if "<velocitycommand" in response["data"].keys():
                    self.joint_commands[
                        int(re.search(r"\[([A-Za-z0-9_]+)]", response["device"]).group(1))] = \
                        response["data"]["<velocitycommand"]
                    logging.error(str(response["device"]) + ": " + str(response["data"]["<velocitycommand"]))

    async def send_joint_states(self, websocket):
        for i, state in enumerate(self.joint_states, 1):
            await websocket.send(json.dumps(
                {
                    "type": "SimDevice",
                    "device": "VelocityJointMotor[" + str(i) + "]",
                    "data": {
                        ">position": state[0],
                        ">velocity": state[1],
                        "<veloitycommand": 0
                    }
                })
            )
        await asyncio.sleep(0.01)

    async def set_joint_commands(self):
        logging.info("attempting to connect to server...")
        async with websockets.connect(self.uri) as websocket:
            logging.info("connected to server!")
            while True:
                response_json = await websocket.recv()
                logging.info("received response from websocket")
                self.parse_responses(json.loads(response_json))
                await self.send_joint_states(websocket)
                await asyncio.sleep(0.01)
