import asyncio

from pybullet_envs.bullet.motor import MotorModel


class ElectricalModel:

    def __init__(self, log, numMotors):
        self.numJoints = numMotors
        self.motors = [MotorModel(torque_control_enabled=True)] * numMotors
        self.joint_actions = [0] * numMotors
        self.joint_states = [{"jointPosition": 0, "jointVelocity": 0}] * numMotors
        self.joint_action = [0] * numMotors
        self.joint_commands = [0] * numMotors
        self.log = log

    def set_joint_commands(self, joint_commands):
        self.joint_commands = joint_commands
        self.log.update_value("commands", self.joint_commands)

    def set_joint_states(self, joint_states):
        self.joint_states = joint_states
        self.log.update_value("positions", list([x[0] for x in self.joint_states]))
        self.log.update_value("velocities", list([x[1] for x in self.joint_states]))

    def get_joint_actions(self):
        self.log.update_value("torques", self.joint_actions)
        return self.joint_actions

    def electrical_sim_loop(self):
        for x in range(self.numJoints):
            _, self.joint_actions[x] = self.motors[x].convert_to_torque(self.joint_commands[x], self.joint_states[x][0],
                                                                self.joint_states[x][1])
        print("Torque: " + str(self.joint_actions))
