from docking_station import DockingStation
from robot import Robot
from flame import Flame


def is_robot(object):
    if isinstance(object, Robot):
        return True
    return False


def is_water_station(object):
    if isinstance(object, DockingStation):
        return True
    return False

