from agent import Agent
import random


class Robot(Agent):

    def __init__(self, position: tuple[int, int]):
        super().__init__(position)
        self.orientation = "^"
        self.battery_life = 100

    def decide(self, percept: dict[tuple[int, int], ...]):
        # # Check if the robot is next to a water station
        # water_stations = [pos for pos, obj in percept.items() if utils.is_water_station(obj)]
        # if water_stations:
        #     # Record the water station's position
        #     self.water_station_location = water_stations[0]
        #
        # empty_spaces = [pos for pos, obj in percept.items() if obj == " "]
        # if empty_spaces:
        #     valid_options = []
        #     move_to = random.choice(empty_spaces)
        #     return "move", move_to

        valid_options = []

        # Define allowed movement based on orientation
        movement_directions = {
            "^": (self.position[0], self.position[1] - 1),  # Up
            "v": (self.position[0], self.position[1] + 1),  # Down
            "<": (self.position[0] - 1, self.position[1]),  # Left
            ">": (self.position[0] + 1, self.position[1])  # Right
        }

        forward_position = movement_directions.get(self.orientation)

        if forward_position in percept and percept[forward_position] == " ":
            valid_options.append(("move", forward_position))

        possible_orientations = ["^", ">", "v", "<"]
        possible_orientations.remove(self.orientation)

        for new_orientation in possible_orientations:
            valid_options.append(("turn", new_orientation))
        chosen_move = random.choice(valid_options)

        return chosen_move


    def act(self, environment):
        cells = self.sense(environment)
        decision = self.decide(cells)

        if decision:
            action, target = decision
            if action == "move":
                self.move(environment, target)
            elif action == "turn":
                self.turn(environment, target)

    def turn(self, environment, turn_to):
        if self.battery_life <= 0:
            print("battery life has ran out")
            exit()
        if environment.turn_to(self.position, turn_to):
            self.orientation = turn_to
            self.battery_life = self.battery_life - 1
            print(f"Robot turned to {self.orientation}")
            print(f"The battery life is {self.battery_life}")

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

