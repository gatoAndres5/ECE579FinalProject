import random

from obstacle.obstacle import Obstacle
class ObstacleManager:
    def __init__(self, spawnRate, obstacles=None):
        self.spawnRate = spawnRate
        if obstacles:
            self.obstacles = obstacles
        else:
            self.obstacles = []
        self.nextId = 1
    
    def addObstacle(self, id, edge):
        obstacle = Obstacle(id, edge)
        obstacle.apply()
        self.obstacles.append(obstacle)
        print(f"Obstacle {id} added on edge {edge.name}")


    def removeObstacle(self, id):
        for obstacle in self.obstacles:
                    if obstacle.obstacleID == id:
                        obstacle.remove()  # unblock the edge
                        self.obstacles.remove(obstacle)
                        print(f"Obstacle {id} removed")
                        return
                    
    def maybeSpawn(self, graph):
        # Decide if we spawn
        if random.random() < self.spawnRate:
            edge = random.choice(graph.edges)

            # Avoid double-blocking same edge
            if not edge.isPassable:
                return None

            obstacle = Obstacle(self.nextId, edge)
            obstacle.apply()
            self.obstacles.append(obstacle)

            print(f"Spawned obstacle {self.nextId} on edge {edge.name}")

            self.nextId += 1
            return obstacle

        return None