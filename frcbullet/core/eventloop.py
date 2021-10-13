import asyncio
import frcbullet.core as fb

class EventLoop:

    def __init__(self):
        self.log = fb.Log("commands", "torques", "positions", "velocities")  # Creates a log table that has four columns
        self.robotModel = fb.BulletModel("/home/henry/PycharmProjects/frcbullet/examples/diff-drive/robot.urdf", True)
        self.wsInterface = fb.WSInterface(self.robotModel.numJoints)

    async def run(self):
        await asyncio.gather(self.wsInterface.set_joint_commands(),
                             self.bulletSimLoop(),
                             self.log.write_to_dataframe())

    async def bulletSimLoop(self):
        while True:
            self.robotModel.set_joint_actions(self.wsInterface.get_joint_commands())
            self.robotModel.update_model()
            self.robotModel.update_logs(self.log)
            await asyncio.sleep(0.01)

