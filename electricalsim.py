import asyncio

from pybullet_envs.bullet.motor import MotorModel


class ElectricalModel:

    def __init__(self, joint_state_queue: asyncio.Queue, joint_action_queue: asyncio.Queue,
                 joint_command_queue: asyncio.Queue, log):
        self.joint_state_queue = joint_state_queue
        self.joint_action_queue = joint_action_queue
        self.joint_command_queue = joint_command_queue
        self.motor = MotorModel(torque_control_enabled=True)
        self.joint_state = 0
        self.joint_action = 0
        self.joint_command = 0
        self.log = log

    async def schedule(self):
        await asyncio.gather(
            self.consume_joint_commands(),
            self.consume_joint_states(),
            self.produce_joint_actions(),
            self.electrical_sim_loop()
        )

    async def consume_joint_commands(self):
        while True:
            self.joint_command = await self.joint_command_queue.get()
            self.log.update_value("command", self.joint_command)
            await asyncio.sleep(0.005)

    async def consume_joint_states(self):
        while True:
            self.joint_state = await self.joint_state_queue.get()
            self.log.update_value("position", self.joint_state["jointPosition"])
            self.log.update_value("velocity", self.joint_state["jointVelocity"])
            await asyncio.sleep(0.005)

    async def produce_joint_actions(self):
        while True:
            await self.joint_action_queue.put(self.joint_action)
            self.log.update_value("torque", self.joint_action)
            await asyncio.sleep(0.01)

    async def electrical_sim_loop(self):
        while True:
            self.joint_action, _ = self.motor.convert_to_torque(self.joint_command, self.joint_state["jointPosition"],
                                                                self.joint_state["jointVelocity"])
            print("Torque: " + str(self.joint_action))
            await asyncio.sleep(0.01)
