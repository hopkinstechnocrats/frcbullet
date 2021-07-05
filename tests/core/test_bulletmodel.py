import pytest
import pytest_mock
import pybullet as p
import os

from frcbullet.core import BulletModel


@pytest.fixture(autouse=True)
def close_bullet_engine():
    if p.isConnected():
        p.resetSimulation()
        p.disconnect()


@pytest.fixture
def bullet_model():
    return BulletModel(os.path.abspath("tests/resources/test-robot/robot.urdf"), False)


def test_init_correct_joints(bullet_model):
    assert p.getNumJoints(bullet_model.robotID) == 1


def test_update_model_steps_simulation(bullet_model, mocker):
    mocker.patch("pybullet.stepSimulation")
    bullet_model.update_model()
    p.stepSimulation.assert_called_once()


def test_get_joint_states(bullet_model):
    expected = p.getJointStates(bodyUniqueId=bullet_model.robotID, jointIndices=range(bullet_model.numJoints))
    actual = bullet_model.get_joint_states()
    assert expected == actual


@pytest.mark.parametrize("update", [x / 10.0 for x in range(10)])
def test_set_joint_actions_changes_velocities(bullet_model, update, mocker):
    mocker.patch('pybullet.setJointMotorControlArray')
    joint_update = [update] * bullet_model.numJoints
    bullet_model.set_joint_actions(joint_update)
    bullet_model.update_model()
    actual = []
    p.setJointMotorControlArray.assert_called_once_with(bodyIndex=bullet_model.robotID,
                                                        jointIndices=range(bullet_model.numJoints),
                                                        controlMode=p.TORQUE_CONTROL,
                                                        forces=joint_update)
