﻿import robot
from agent import Agent
import utils

class DockingStation(Agent):

    def __init__(self, position):
        super().__init__(position)
        self.orientation = "u"

    def decide(self, percept):
        sensed_spaces = {
            "u": (self.position[0], self.position[1] - 1),  # Up
            "d": (self.position[0], self.position[1] + 1),  # Down
            "l": (self.position[0] - 1, self.position[1]),  # Left
            "r": (self.position[0] + 1, self.position[1])  # Right
        }

        for space in percept:
            if utils.is_robot(space):
                return True
            else:
                return False

    def act(self, environment):
        cell = self.sense(environment)
        decision = self.decide(cell)
        if decision:
            robot.water_level = 100


    def __str__(self):
        return self.orientation
