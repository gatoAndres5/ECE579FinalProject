from robot.robot import Robot
from routing.path_planner import PathPlanner

class Fleet_Manager:
    def __init__(self, fw, environment_graph, true_obstacles, path_planner):
        self.robots = []
        self.nextRobotID = 0 # next robot added will have this ID
        self.fw = fw
        self.eg = environment_graph
        self.true_obstacles = true_obstacles
        self.planner = path_planner
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
    
    def calculatePathCost(self, path):
        if not path or len(path) < 2:
            return 0
            
        total_cost = 0
        for i in range(len(path) - 1):
            current_node = path[i]
            next_node = path[i + 1]
            for edge in current_node.edges:
                if edge.destNode == next_node:
                    total_cost += edge.cost
                    break
                    
        return total_cost

    # dispatch an order, given bags from FoodieBagger
    def dispatchOrder(self, order, bags):
        # dispatch to first available robot
        
        if not bags:
            print(f"Error: attempting to dispatch order with no bags.")
            return

        r = None
        for robot in self.robots:
            if robot.getStatus() == "ready":
                destination = order.getDestination()
                path_out = self.planner.calculate_path(self.fw, destination)
                if not path_out:
                    continue
                cost_out = self.calculatePathCost(path_out)

                path_back = self.planner.calculate_path(destination, self.fw)
                if not path_back:
                    continue
                cost_back = self.calculatePathCost(path_back)

                total_min_cost = cost_out + cost_back
                min_battery = total_min_cost * 1

                buffer = min_battery * 0.2
                if robot.getBattery() >= min_battery + buffer:
                    if bags:
                        if len(robot.bags) + len(bags) <= robot.getCapacity():
                            r = robot
                        else:
                            # no capacity for this order
                            continue
                    r = robot
                    print(f"Selected robot {r.getID()} to dispatch.")
                    break

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

    # TODO multiple orders
    # check capacity - can these orders fit
    # but don't want to assign and keep a robot waiting
    # given a set of orders (in ordermanager) how to optimize which orders go to which robot