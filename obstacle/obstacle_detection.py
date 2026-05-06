from collections import deque
class ObstacleDetection:
    def __init__(self, obstacles=None, sensorRange=0):
        if obstacles:
            self.obstacles = obstacles
        else: 
            self.obstacles = []
        self.sensorRange = sensorRange
    
    # Checking if any obstacle is on this edge
    def isObstacle(self, edge):
        for obstacle in self.obstacles:
            if obstacle.getEdge() == edge:
                return True
        return False 
    
    # Using number of hops BFS style, used AI tools for this algorithm to simluate a sensor
    def sense(self, currentNode):
        detected = []
        visited = set()
        queue = deque([(currentNode, 0)])

        while queue:
            node, dist = queue.popleft()

            if dist > self.sensorRange:
                continue

            if node in visited:
                continue

            visited.add(node)

            for edge in node.edges:
                # Check for obstacle first
                if self.isObstacle(edge):
                    obstacle = next(
                        o for o in self.obstacles
                        if o.getEdge() == edge
                    )
                    detected.append(obstacle)

                # Only traverse farther if edge is still passable
                if edge.isPassable:
                    queue.append((edge.destNode, dist + 1))

        return detected
    
    def triggerPathRecalculation(self, planner, currentNode, goalNode):
        detected = self.sense(currentNode, goalNode)
        if not detected:
            return None
        
        for obstacle in detected:
            obstacle.apply()

        new_path = planner.calculate_path(currentNode, goalNode)
        return new_path