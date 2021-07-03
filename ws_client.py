import asyncio
import json
import websockets


async def get_joint_commands(joint_command_queue: asyncio.Queue):
    uri = "ws://localhost:3300/wpilibws"
    async with websockets.connect(uri) as websocket:
        devices = []
        while True:
            response_json = await websocket.recv()
            response = json.loads(response_json)
            if response["type"] == "PWM":
                if response["device"] not in devices:
                    devices.append(response["device"])
                if response["device"] == '0':
                    if "<speed" in response["data"].keys():
                        await joint_command_queue.put(response["data"]["<speed"])


async def print_msg(websocket):
    print(await websocket.recv())


if __name__ == "__main__":
    asyncio.run(get_joint_commands(asyncio.Queue()))
