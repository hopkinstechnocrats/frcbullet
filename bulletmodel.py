import pybullet as p
import pybullet_data
import asyncio


class BulletModel:

    def __init__(self, urdf_location, joint_action_queue: asyncio.Queue, joint_state_queue: asyncio.Queue):
        physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        p.setGravity(0, 0, -10)
        planeId = p.loadURDF("plane.urdf")
        startPos = [0, 0, 0]
        startOrientation = p.getQuaternionFromEuler([0, 0, 0])
        self.robotID = p.loadURDF(urdf_location, startPos, startOrientation, useFixedBase=1)
        self.joint_action_queue = joint_action_queue
        self.joint_state_queue = joint_state_queue
        self.joint_torque = 0
        self.joint_position = 0
        self.joint_velocity = 0

    async def schedule(self):
        await asyncio.gather(
            self.consume_joint_actions(),
            self.produce_joint_states(),
            self.update_model()
        )

    async def consume_joint_actions(self):
        while True:
            joint_update = await self.joint_action_queue.get()
            self.joint_torque = joint_update
            self.joint_action_queue.task_done()
            await asyncio.sleep(0.005)

    async def produce_joint_states(self):
        while True:
            joint_state = p.getJointState(bodyUniqueId=self.robotID, jointIndex=0)
            self.joint_position = joint_state[0]
            self.joint_velocity = joint_state[0]
            await self.joint_state_queue.put(
                {"jointPosition": self.joint_position, "jointVelocity": self.joint_velocity})
            await asyncio.sleep(0.01)

    async def update_model(self):
        p.setJointMotorControl2(bodyIndex=self.robotID,
                                jointIndex=0,
                                controlMode=p.VELOCITY_CONTROL,
                                force=0)
        while True:
            p.setJointMotorControl2(bodyIndex=self.robotID,
                                    jointIndex=0,
                                    controlMode=p.TORQUE_CONTROL,
                                    force=self.joint_torque)
            p.stepSimulation()
            await asyncio.sleep(10. / 240.)
            cubePos, cubeOrn = p.getBasePositionAndOrientation(self.robotID)
            # print(cubePos, cubeOrn)
