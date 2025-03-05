from xml.etree.ElementTree import tostring

import robot
from agent import Agent
import utils

class DockingStation(Agent):

    def __init__(self, position):
        super().__init__(position)
        self.orientation = "u"
        self.sensed_spaces = {
            "u": (self.position[0], self.position[1] - 1),  # Up
            "d": (self.position[0], self.position[1] + 1),  # Down
            "l": (self.position[0] - 1, self.position[1]),  # Left
            "r": (self.position[0] + 1, self.position[1])  # Right
        }

    def decide(self, percept):
        forward_space = self.sensed_spaces.get(self.orientation)
        if forward_space in percept and utils.is_robot(percept[forward_space]):
            return True
        return False

    def act(self, environment):
        cell = self.sense(environment)
        decision = self.decide(cell)
        forward_space = self.sensed_spaces.get(self.orientation)

        if decision:
         robot_instance = cell[forward_space]
         robot_instance.battery_life  = min(robot_instance.battery_life + 5, 100)


    def __str__(self):
        return self.orientation
