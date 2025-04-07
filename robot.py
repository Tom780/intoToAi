from agent import Agent
import random
import utils
import heapq

from docking_station import DockingStation


class Robot(Agent):

    def __init__(self, position: tuple[int, int],map_size = (30,17)):
        super().__init__(position)
        self.orientation = "^"
        self.battery_life = 100
        self.current_location = position
        self.map_size = map_size
        self.map = [["?" for _ in range(map_size[1])] for _ in range(map_size[0])]

    def decide(self, percept: dict[tuple[int, int], ...],environment):
        valid_options = []

        movement_directions = {
            "^": (self.position[0], self.position[1] - 1),
            "v": (self.position[0], self.position[1] + 1),
            "<": (self.position[0] - 1, self.position[1]),
            ">": (self.position[0] + 1, self.position[1])
        }

        forward_position = movement_directions.get(self.orientation)
        chosen_move = None
        current_dirt = environment.get_dirt_level(self.position)

        if self.battery_life <= 30:
            path = self.calc_path(self.position, (3, 10), ["x"])
            if path and len(path) > 1:
                next_move = path[1]
                if next_move == forward_position:
                    chosen_move = ("move",next_move)
                else:
                    for direction,pos in movement_directions.items():
                        if pos == next_move:
                            chosen_move = ("turn",direction)
                            break

        elif current_dirt > 0:
            print(f"The robot is about to clean tile {self.position}")
            chosen_move = ("clean",self.position)

        else:
            if self.position == (3,10) and self.battery_life < 100:
                chosen_move = ("charge",self.position[0])
            else:
                max_dirt = -1
                tile_to_move_to = None
                for pos in percept:
                    if isinstance(percept[pos], str) and percept[pos] == " ":
                        dirt = environment.get_dirt_level(pos)
                        if dirt > max_dirt:
                            max_dirt = dirt
                            tile_to_move_to = pos

                if tile_to_move_to == forward_position:
                    return "move",tile_to_move_to

                for direction, pos in movement_directions.items():
                    if pos == tile_to_move_to:
                        return "turn", direction

                if forward_position in percept and isinstance(percept[forward_position], tuple) and \
                        percept[forward_position][0] == " ":
                    valid_options.append(("move", forward_position))

                possible_orientations = ["^", ">", "v", "<"]
                possible_orientations.remove(self.orientation)

                for new_orientation in possible_orientations:
                    valid_options.append(("turn", new_orientation))
                chosen_move = random.choice(valid_options)

        return chosen_move


    def act(self, environment):
        cells = self.sense(environment)
        for pos, value in cells.items():
            x, y = pos
            if isinstance(value, str):
                self.map[y][x] = value
            elif isinstance(value, DockingStation):
                if utils.is_docking_station(value):
                    self.map[y][x] = value.orientation
                else:
                    self.map[y][x] = str(value)


        decision = self.decide(cells, environment)

        if decision:
            action, target = decision
            if action == "move":
                self.move(environment, target)
            elif action == "turn":
                self.turn(environment, target)
            elif action == "charge":
                self.charge()
            elif action == "return to docking":
                self.return_to_docking(environment)
            elif action == "clean":
                environment.clean_cell(self.position)
                self.battery_life -= 2
                print(f"The battery life of the robot after cleaning is: {self.battery_life}")

    def return_to_docking(self,environment):
        path = self.calc_path(self.position,(3,10),["x"])
        self.move(environment,path[0])

    def charge(self):
        print("the battery has increased")
        print(f"The battery life is {self.battery_life}")


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

        # MANHATTAN DISTANCE FUNCTIONS

    def calc_path(self, start, goal, avoid):
        p_queue = []
        heapq.heappush(p_queue, (0, start))

        directions = {
            "right": (0, 1),
            "left": (0, -1),
            "up": (-1, 0),
            "down": (1, 0)
        }
        predecessors = {start: None}
        g_values = {start: 0}

        while len(p_queue) != 0:
            current_cell = heapq.heappop(p_queue)[1]
            if current_cell == goal:
                return self.get_path(predecessors, start, goal)
            for direction in ["up", "right", "down", "left"]:
                row_offset, col_offset = directions[direction]
                neighbour = (current_cell[0] + row_offset, current_cell[1] + col_offset)

                if self.viable_move(neighbour[0], neighbour[1], avoid) and neighbour not in g_values:
                    cost = g_values[current_cell] + 1
                    g_values[neighbour] = cost
                    f_value = cost + self.calc_distance(goal, neighbour)
                    heapq.heappush(p_queue, (f_value, neighbour))
                    predecessors[neighbour] = current_cell

    def get_path(self, predecessors, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = predecessors[current]
        path.append(start)
        path.reverse()
        return path

    def viable_move(self, x, y, types):
        return (x, y) not in types



    def calc_distance(self, point1: tuple[int, int], point2: tuple[int, int]):
        x1, y1 = point1
        x2, y2 = point2
        return abs(x1 - x2) + abs(y1 - y2)

    # END OF MANHATTAN DISTANCE FUNCTIONS
    def output_map(self):
        out = ""
        for row in self.map:
            for col in row:
                out += f"{col}\t"
            out += "\n"
        return out

    def __str__(self):
        return self.orientation
