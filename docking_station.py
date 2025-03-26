from agent import Agent
import utils

class DockingStation(Agent):

    def __init__(self, position):
        super().__init__(position)
        self.orientation = "u"
        self.sensed_spaces = {
            "u": (self.position[0], self.position[1] - 1),
            "d": (self.position[0], self.position[1] + 1),
            "l": (self.position[0] - 1, self.position[1]),
            "r": (self.position[0] + 1, self.position[1])
        }
        self.senses_robot = False

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
         self.senses_robot = True
         print("The robot instance is", robot_instance)
         robot_instance.battery_life  = min(robot_instance.battery_life + 5, 100)


    def __str__(self):
        return self.orientation
