from robot.robot import Robot

class Fleet_Manager:
    def __init__(self):
        self.robots = []
        self.nextRobotID = 0 # next robot added will have this ID

    def addRobot(self):
        self.robots.append(Robot(self.nextRobotID))
        self.nextRobotID += 1

    def hasAvailableRobot(self):
        for robot in self.robots:
            if robot.getStatus() == "ready":
                return True
        return False

    def assignOrder(self, order):
        # dispatch to first available robot
        for robot in self.robots:
            if robot.getStatus() == "ready":
                robot.assignOrder(order)
                return robot.getID()
        print("Error: no robot available to assign order")
        return None

    # where is this called from?
    def completeOrder(self, robotID):
        for robot in self.robots:
            if robot.id == robotID:
                robot.completeOrder()
                break
    
