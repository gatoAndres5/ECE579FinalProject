from robot import Robot

class Fleet_Manager:
    def __init__(self):
        self.robots = []

    def addRobot(self, robot):
        self.robots.append(robot)

    def assignOrder(self, robotID, order):
        for robot in self.robots:
            if robot.id == robotID:
                robot.assignOrder(order)
                break

    def completeOrder(self, robotID):
        for robot in self.robots:
            if robot.id == robotID:
                robot.completeOrder()
                break
    
