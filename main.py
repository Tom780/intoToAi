from environment import Environment

if __name__ == "__main__":
    e = Environment("floorplan.txt")

    docking = e.world[11][3]
    robot1 = e.world[10][3]

    print("The starting position is:")
    print(e)

    print("The battery life of the robot is: ", robot1.battery_life)
    for i in range(100):
        robot1.act(e)
        docking.act(e)
        print(e)
    print("The robots map at the end was")
    print (robot1.output_map())