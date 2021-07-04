import asyncio

import pytest
import websockets
import frcbullet.core as fb


def test_get_joint_commands_connects_to_websocket(mocker):
    mocker.patch('websockets.connect')
    joint_command_queue = asyncio.Queue()
    with pytest.raises(Exception):
        asyncio.run(asyncio.wait_for(fb.get_joint_commands(joint_command_queue),1))
    websockets.connect.assert_called_once()
