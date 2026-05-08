class Edge:
    def __init__(self, edgeID, cost, originNode, destNode, isPassable, name=None):
        self.edgeID = edgeID
        if name:
            self.name = name
        else:
            self.name = f"Edge{edgeID}"
        self.cost = cost
        self.originNode = originNode
        self.destNode = destNode
        self.isPassable = isPassable
        originNode.edges.append(self)
        destNode.edges.append(self)

    def getCost(self):
        return self.cost

    def setPassibility(self, passable):
        self.isPassable = passable
