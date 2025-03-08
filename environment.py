import utils


class Environment:

    def __init__(self, map_path):
        self.file_path = map_path
        self.world = self.load_assets(self.load_map())

    def load_map(self):
        try:
            with open(self.file_path) as f:
                world_map = [[col.lower() for col in line.strip()] for line in f]

                first_row = len(world_map[0])
                for row in world_map:
                    if len(row) != first_row:
                        raise Exception("Map rows are not even")
                return world_map
        except FileNotFoundError:
            print(f"File not found")
        except PermissionError:
            print(f"File read permissions were denied")
        except IOError as e:
            print(f"IO error: {e}")

        return []

    def load_assets(self, world_map:list):
        for i in range(len(world_map)):
            for j in range(len(world_map[i])):
                if world_map[i][j] == 'u' or world_map[i][j] == 'd' or world_map[i][j] == 'l' or world_map[i][j] == 'r':
                    world_map[i][j] = utils.DockingStation((j, i))
                elif world_map[i][j] == '^' or world_map[i][j] == 'v' or world_map[i][j] == '<' or world_map[i][j] == '>':
                    world_map[i][j] = utils.Robot((j, i))
        return world_map


    def get_cells(self, positions:list) -> dict[tuple[int,int],...]:
        cells = {}
        for pos in positions:
            cells[pos] = self.world[pos[1]][pos[0]]
        return cells


    def move_to(self, position, move_to):
        from_x, from_y = position
        to_x, to_y = move_to

        self.world[to_y][to_x] = self.world[from_y][from_x]
        self.world[from_y][from_x] = " "
        return True


    def turn_to(self, position, turn_to):
        self.world[position[1]][position[0]].orientation = turn_to
        return True


    def __str__(self):
        out = ""
        for row in self.world:
            for col in row:
                out += f"{col}\t"
            out += "\n"
        return out
