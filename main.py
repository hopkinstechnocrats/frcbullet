import asyncio

from bulletmodel import BulletModel
from electricalsim import ElectricalModel
from log import Log
from ws_client import get_joint_commands


async def run():
    joint_action_queue = asyncio.Queue()  # Sends joint torques from ElectricalModel to BulletModel
    joint_state_queue = asyncio.Queue()  # Sends joint states (position, velocity) from BulletModel to ElectricalModel
    joint_command_queue = asyncio.Queue()  # Sends joint commands (percent output) from the WebSocket client to the
    # ElectricalModel
    log = Log("command", "torque", "position", "velocity")  # Creates a log table that has four columns
    robotModel = BulletModel("test-robot/robot.urdf", joint_action_queue, joint_state_queue)
    electricalModel = ElectricalModel(joint_state_queue, joint_action_queue, joint_command_queue, log)

    # Four coroutines contain loops and are run in parallel:
    await asyncio.gather(
        get_joint_commands(joint_command_queue),
        robotModel.schedule(),
        electricalModel.schedule(),
        log.schedule()
    )


if __name__ == '__main__':
    asyncio.run(run())
