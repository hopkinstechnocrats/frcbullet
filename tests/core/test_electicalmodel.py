import pytest

from frcbullet.core import ElectricalModel


@pytest.fixture
def electrical_model():
    return ElectricalModel()
