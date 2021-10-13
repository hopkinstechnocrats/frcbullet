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
        self.robotID = p.loadURDF(urdf_location, startPos, startOrientation)
        self.numJoints = p.getNumJoints(self.robotID)
        p.setJointMotorControlArray(bodyIndex=self.robotID,
                                    jointIndices=range(self.numJoints),
                                    controlMode=p.VELOCITY_CONTROL,
                                    forces=[0] * self.numJoints)
        self.joint_velocity_command_array = [0] * self.numJoints
        self.max_forces = [3] * self.numJoints
        self.joint_position = [0] * self.numJoints
        self.joint_velocity = [0] * self.numJoints

    def set_joint_actions(self, joint_update):
        self.joint_velocity_command_array = joint_update

    def get_joint_states(self):
        return p.getJointStates(bodyUniqueId=self.robotID, jointIndices=range(self.numJoints))

    def update_model(self):
        p.setJointMotorControlArray(bodyIndex=self.robotID,
                                    jointIndices=range(self.numJoints),
                                    controlMode=p.VELOCITY_CONTROL,
                                    targetVelocities=self.joint_velocity_command_array,
                                    forces=self.max_forces)
        p.stepSimulation()

    def update_logs(self, log):
        log.update_value("commands", self.joint_velocity_command_array)
        joint_states = p.getJointStates(self.robotID, range(self.numJoints))
        log.update_value("torques", list(map(lambda x: x[3], joint_states)))
        log.update_value("velocities", list(map(lambda x: x[1], joint_states)))
        log.update_value("positions", list(map(lambda x: x[0], joint_states)))
