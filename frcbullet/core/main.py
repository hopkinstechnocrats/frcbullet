import frcbullet.core as fb
import asyncio

async def run():
    joint_action_queue = asyncio.Queue()  # Sends joint torques from ElectricalModel to BulletModel
    joint_state_queue = asyncio.Queue()  # Sends joint states (position, velocity) from BulletModel to ElectricalModel
    joint_command_queue = asyncio.Queue()  # Sends joint commands (percent output) from the WebSocket client to the
    # ElectricalModel
    log = fb.Log("command", "torque", "position", "velocity")  # Creates a log table that has four columns
    robotModel = fb.BulletModel("test-robot/robot.urdf", joint_action_queue, joint_state_queue)
    electricalModel = fb.ElectricalModel(joint_state_queue, joint_action_queue, joint_command_queue, log)

    # Four coroutines contain loops and are run in parallel:
    await asyncio.gather(
        fb.get_joint_commands(joint_command_queue),
        robotModel.schedule(),
        electricalModel.schedule(),
        log.schedule()
    )


if __name__ == '__main__':
    asyncio.run(run())
