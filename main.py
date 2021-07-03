import asyncio

from bulletmodel import BulletModel
from electricalsim import ElectricalModel
from log import Log
from ws_client import get_joint_commands


async def run():
    joint_action_queue = asyncio.Queue()
    joint_state_queue = asyncio.Queue()
    joint_command_queue = asyncio.Queue()
    log = Log("command", "torque", "position", "velocity")
    robotModel = BulletModel("test-robot/robot.urdf", joint_action_queue, joint_state_queue)
    electricalModel = ElectricalModel(joint_state_queue, joint_action_queue, joint_command_queue, log)
    await asyncio.gather(
        get_joint_commands(joint_command_queue),
        robotModel.schedule(),
        electricalModel.schedule(),
        log.schedule()
    )


if __name__ == '__main__':
    asyncio.run(run())
