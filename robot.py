from agent import Agent
import random
import environment

class Robot(Agent):

    def __init__(self, position: tuple[int, int],map_size = (30,17)):
        super().__init__(position)
        self.orientation = "^"
        self.battery_life = 80
        self.current_location = position
        self.charge_location = [10][3]
        self.map_size = map_size
        self.map = [["?" for _ in range(map_size[1])] for _ in range(map_size[0])]






    def decide(self, percept: dict[tuple[int, int], ...]):
        valid_options = []

        movement_directions = {
            "^": (self.position[0], self.position[1] - 1),
            "v": (self.position[0], self.position[1] + 1),
            "<": (self.position[0] - 1, self.position[1]),
            ">": (self.position[0] + 1, self.position[1])
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
