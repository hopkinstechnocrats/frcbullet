import asyncio
import json
import time
import pytest
import websockets
import frcbullet.core as fb

#
#
# async def mock_server_func(websocket, path):
#     await websocket.send(json.dumps({
#         "type": "PWM",
#         "device": 0,
#         "data": {
#             "<init": True,
#             "<speed": 0.25
#         }
#     }))
#
# def mock_wpilib_server():
#     return websockets.serve(mock_server_func, "localhost", 3300)
#
# @pytest.fixture
# def cleanup():
#     asyncio.get_event_loop().close()
#     yield
#     asyncio.get_event_loop().close()
#
#
# def test_sends_single_motor_signal():
#     ws_interface = fb.WSInterface(1)
#     loop = asyncio.get_event_loop()
#     loop.run_until_complete(mock_wpilib_server())
#     loop.run_until_complete(ws_interface.set_joint_commands())
#     time.sleep(1)
#     loop.stop()
#     assert ws_interface.get_joint_commands() == [0.25]
