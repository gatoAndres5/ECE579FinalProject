from obstacle.obstacle_detection import ObstacleDetection
from routing.path_planner import PathPlanner

class Movement_Controller:
    def __init__(self, robot, environment_graph, true_obstacles):
        self.robot = robot
        self.planner = PathPlanner(environment_graph) # each needs own pathPlanner since PP stores a single path
        self.obstacleSensor = ObstacleDetection(obstacles=true_obstacles) # TODO need to pass true list of obstacles
        self.distanceTravelled = 0
        self.destinationNode = None
        self.currentPath = None
        self.activeItinerary = []
        self.currentTargetOrder = None

    def setItinerary(self, orders):
        # called by FM
        self.activeItinerary = self.optimizeItinerary(orders)

        self.targetNextDestination()

    def optimizeItinerary(self, orders):
        # Used AI tools to help implement the code for a greedy nearest-neighbor algorithm to optimize an order 
        # itinerary
        unvisited = orders[:]
        currentNode = self.robot.getPosition()
        optimizedQueue = []
        
        while unvisited:
            bestOrder = None
            bestCost = float('inf')

            for order in unvisited:
                # A* to find path
                path = self.planner.calculate_path(currentNode, order.getDestination())

                cost = float('inf')
                if path:
                    cost = self.planner.calculatePathCost(path)

                if cost < bestCost:
                    bestCost = cost
                    bestOrder = order

            if not bestOrder:
                print("Warning: some destinations are not visitable")
                break
            optimizedQueue.append(bestOrder)
            currentNode = bestOrder.getDestination() # assume navigated to this path
            unvisited.remove(bestOrder)
        return optimizedQueue

    def targetNextDestination(self):
        if not self.activeItinerary:
            # send back to FW
            self.currentTargetOrder = None
            self.destinationNode = self.robot.fm.fw
        else:
            # goto next order in the queue
            self.currentTargetOrder = self.activeItinerary.pop(0)
            self.destinationNode = self.currentTargetOrder.getDestination()

        path = self.planner.calculate_path(self.robot.getPosition(), self.destinationNode)

        if not path:
            print(f"Error: robot {self.robot.getID()} failed to find a path to {self.destinationNode.name}")
            return False
        
        print(f"Robot {self.robot.getID()} targeting next path to {self.destinationNode.name}")
        return True

    def getDestination(self):
        return self.destinationNode
    
    def getDistanceTravelled(self):
        return self.distanceTravelled
    
    # set the current destination for the robot
    def setDestination(self, destination):
        self.destinationNode = destination
        
        # calculate path
        path = self.planner.calculate_path(self.robot.getPosition(), destination)
        self.currentPath = path

        if not path:
            print(f"Error: robot {self.robot.getID()} failed to find a path to {destination.name}")
            return False
        return True
    
    def step(self):
        # call once per tick. True if arrived at destination, False otherwise
        if not self.planner.current_path and self.robot.getPosition() == self.destinationNode:
            return "COMPLETE" 
        
        currentNode = self.robot.getPosition()

        # sense for obstacles
        detectedObstacles = self.obstacleSensor.sense(currentNode)
        foundNewObstacles = False
        for obstacle in detectedObstacles:
            e = obstacle.getEdge()
            if e.isPassable: # new obstacle - passability not yet updated
                e.setPassibility(False)
                foundNewObstacles = True
                print(f"Robot {self.robot.getID()}: sensed a new obstacle.")
                # TODO can report back to the Fleet Manager to trigger other Robots to check path for this new edge
                # to update before they discover the obstacle in their path

        if foundNewObstacles:
            print(f"Robot {self.robot.getID()} recalculating path...")
            newPath = self.planner.calculate_path(currentNode, self.destinationNode)
            if not newPath:
                print(f"Error: robot {self.robot.getID()} cannot find a new path.")
                return "FAIL"
            print(f"Robot {self.robot.getID()} found a new path.")

        # move one unit per step
        if self.planner.current_path:
            nextNode = self.planner.current_path.pop(0)

            if nextNode == currentNode and self.planner.current_path:
                # if already at the next node, move forward again
                nextNode = self.planner.current_path.pop(0)

            self.robot.position = nextNode
            self.distanceTravelled += 1
            print(f"Robot {self.robot.getID()}: moved to Node {nextNode.name}")

        if self.robot.position == self.destinationNode:
            # arrived at destination
            print(f"Robot {self.robot.getID()} arrived at destination {self.destinationNode.name}")
            return "COMPLETE"
        return "MOVING"
