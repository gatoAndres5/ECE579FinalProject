from obstacle.obstacle_detection import ObstacleDetection
from routing.path_planner import PathPlanner

class Movement_Controller:
    def __init__(self, robot, environment_graph, true_obstacles):
        self.robot = robot
        self.planner = PathPlanner(environment_graph) # each needs own pathPlanner since PP stores a single path
        self.obstacleSensor = ObstacleDetection(obstacles=true_obstacles) # TODO need to pass true list of obstacles
        self.distanceTravelled = 0

    def moveTo(self, destinationNode):
        path = self.planner.calculate_path(self.robot.getPosition(), destinationNode)

        if not path:
            print(f"Error: {self.robot.getID()} cannot find an initial path.")
            return False
        
        return self.executePath(destinationNode)
    
    def executePath(self, destinationNode):
        while self.planner.current_path:
            currentNode = self.robot.getPosition()

            detectedObstacles = self.sensor.sense(currentNode)
            print(f"{self.robot.getID()} found an obstacle")

            foundNewObstable = False
            # update the environment graph
            for obstacle in detectedObstacles:
                e = obstacle.getEdge()
                if e.isPassable: # new obstacle, edge not yet update
                    e.setPassibility(False)
                    foundNewObstable = True
                    # TODO can report back to Fleet Manager for other robots to check own paths
                
            if foundNewObstable:
                print(f"Robot {self.robot.getID()} sensed new obstacle(s). Recalculate path.")
                newPath = self.planner.calculate_path(currentNode, destinationNode)
                if not newPath:
                    print(f"Error: no new path found.")
                continue;

            # now move to next node (event-based, not time-stepped)
            nextNode = self.planner.current_path.pop(0)
            self.robot.position = nextNode
            print(f"Robot {self.robot.getID()} moved to Node {nextNode.name}")
        
        if self.robot.position == destinationNode:
            print(f"Robot {self.robot.getID()} arrived at destination {destinationNode.name}")
            return True
        else:
            print(f"Error: robot {self.robot.getID()} at wrong location")