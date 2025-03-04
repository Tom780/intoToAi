from agent import Agent
import utils
import random
import heapq
import random

import random


class Robot(Agent):

    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self.orientation = "^"
        self.battery_life = 1

    def decide(self, percept: dict[tuple[int, int], ...]):

        # Check if the robot is next to a water station
        water_stations = [pos for pos, obj in percept.items() if utils.is_water_station(obj)]
        if water_stations:
            # Record the water station's position
            self.water_station_location = water_stations[0]


        empty_spaces = [pos for pos, obj in percept.items() if obj == " "]
        if empty_spaces:
            move_to = random.choice(empty_spaces)
            return "move", move_to

    def act(self, environment):
        cells = self.sense(environment)
        decision = self.decide(cells)

        if decision:
            action, target = decision
            if action == "move":
                self.move(environment, target)

    def move(self, environment, to):
        if self.battery_life <= 0:
            print("battery life has ran out")
            exit()
        else:
            if environment.move_to(self.position, to):
                self.position = to
                self.battery_life = self.battery_life - 1
                print(f"Robot moved to {self.position}")
                print(f"The battery life is {self.battery_life}")

    def __str__(self):
        return self.orientation

