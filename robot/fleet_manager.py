from robot.robot import Robot

class Fleet_Manager:
    def __init__(self, fw, environment_graph, true_obstacles):
        self.robots = []
        self.nextRobotID = 0 # next robot added will have this ID
        self.fw = fw
        self.eg = environment_graph
        self.true_obstacles = true_obstacles
        # TODO would like to not pass true_obstacles, but modify ObstacleManager to return whether there is truly an
        # obstacle when sense() is called

    def addRobot(self, robot=None):
        if robot is not None:
            self.robots.append(robot)
            self.nextRobotID += 1
            return
        r = Robot(self, self.nextRobotID, self.fw, self.eg, self.true_obstacles)
        self.robots.append(r)
        self.nextRobotID += 1

    def hasAvailableRobot(self):
        for robot in self.robots:
            if robot.getStatus() == "ready":
                return True
        return False

    def getAvailableRobot(self):
        for robot in self.robots:
            if robot.getStatus() == "ready":
                return robot
        return None

    # dispatch an order, given bags from FoodieBagger
    def dispatchOrder(self, order, bags):
        # dispatch to first available robot
        r = self.getAvailableRobot()
        if not r:
            print("Error: no robot available to assign order")
            return None

        # assign order
        r.assignOrder(order)

        # load bags
        if bags is not None:
            for b in bags:
                r.addBag(b, r.getPosition())

        # dispatch robot
        r.setDestination(order.getDestination())

        return r

    def completeOrder(self, robotID):
        for robot in self.robots:
            if robot.id == robotID:
                robot.completeOrder()
                break
