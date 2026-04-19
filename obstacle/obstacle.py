class Obstacle:
    def __init__(self, obstacleID, edge):
        self.obstacleID = obstacleID
        self.edge = edge
    
    def getEdge(self):
        return self.edge
    
    def apply(self):
        self.edge.setPassibility(False)

    def remove(self):
        self.edge.setPassibility(True)