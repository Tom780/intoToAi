import utils

from environment import Environment

if __name__ == "__main__":
    e = Environment("floorplan.txt")

    docking = e.world[11][3]
    robot1 = e.world[10][3]

    print("The starting position is:")
    print(e)

    for i in range(5):
        # Change 1 simulate more moves. I.e. 100 would simulate 100 moves
        # Call the act method for each agent operating in the environment

        robot1.act(e)
        docking.act(e)
        print(e)
