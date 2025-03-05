import utils

from environment import Environment

if __name__ == "__main__":
    e = Environment("floorplan.txt")

    docking = e.world[11][3]
    robot1 = e.world[10][3]

    print("The starting position is:")
    print(e)

    while robot1.battery_life != 0:
        robot1.act(e)
        docking.act(e)
        print(e)

    # for i in range(5):
    #     robot1.act(e)
    #     docking.act(e)
    #     print(e)
