from agent import Agent
import utils
import random
import heapq
import random

import random


class Robot(Agent):

    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self.water_level = 100
        self.water_station_location = None
        self.flame_handled = False  # Tracks if the robot has already handled a flame
        self.orientation = "^"
        self.battery_life = 1

    def decide(self, percept: dict[tuple[int, int], ...]):
        flames = [pos for pos, obj in percept.items() if utils.is_flame(obj)]

        # Check if the robot is next to a water station
        water_stations = [pos for pos, obj in percept.items() if utils.is_water_station(obj)]
        if water_stations:
            # Record the water station's position
            self.water_station_location = water_stations[0]

        if flames:
            # If there are flames, pick one at random
            flame_to_tackle = random.choice(flames)
            return "extinguish", flame_to_tackle

        # If the robot's water level is low and it has recorded a water station location, move to the water station
        if self.water_level < 30 and self.water_station_location:
            return "move", self.water_station_location

        # No flames and water level is fine, continue moving randomly
        empty_spaces = [pos for pos, obj in percept.items() if obj == " "]
        if empty_spaces:
            move_to = random.choice(empty_spaces)
            return "move", move_to

    def act(self, environment):
        cells = self.sense(environment)  # Get surrounding cells
        decision = self.decide(cells)  # Decide what to do based on surrounding cells

        if decision:
            action, target = decision
            if action == "extinguish":
                self.extinguish_flame(environment, target)
            elif action == "move":
                self.move(environment, target)

    def extinguish_flame(self, environment, flame_position):
        # Extinguish the flame and reduce water level by 5%
        self.water_level = max(self.water_level - 5, 0)  # Prevent water level from going negative
        environment.world[flame_position[1]][flame_position[0]] = " "  # Remove the flame from the environment
        print(f"Flame at {flame_position} extinguished! Water level: {self.water_level}%")

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

