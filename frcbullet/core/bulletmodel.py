import pybullet as p
import pybullet_data
import asyncio


class BulletModel:

    def __init__(self, urdf_location, gui: bool):
        physicsClient = p.connect(p.GUI if gui else p.DIRECT)  # or p.DIRECT for non-graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath())  # optionally
        p.setGravity(0, 0, -10)
        planeId = p.loadURDF("plane.urdf")
        startPos = [0, 0, 0]
        startOrientation = p.getQuaternionFromEuler([0, 0, 0])
        self.robotID = p.loadURDF(urdf_location, startPos, startOrientation, useFixedBase=1)
        self.numJoints = p.getNumJoints(self.robotID)
        p.setJointMotorControlArray(bodyIndex=self.robotID,
                                    jointIndices=range(self.numJoints),
                                    controlMode=p.VELOCITY_CONTROL,
                                    forces=[0] * self.numJoints)
        self.joint_torque_array = [0] * self.numJoints
        self.joint_position = [0] * self.numJoints
        self.joint_velocity = [0] * self.numJoints

    def set_joint_actions(self, joint_update):
        self.joint_torque_array = joint_update

    def get_joint_states(self):
        return p.getJointStates(bodyUniqueId=self.robotID, jointIndices=range(self.numJoints))

    def update_model(self):
        p.setJointMotorControlArray(bodyIndex=self.robotID,
                                    jointIndices=range(self.numJoints),
                                    controlMode=p.TORQUE_CONTROL,
                                    forces=self.joint_torque_array)
        p.stepSimulation()
