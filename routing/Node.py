class Node:
    def __init__(self, nodeID, name=None, x=0, y=0):
        self.nodeID = nodeID
        if name:
            self.name = name
        else:
            self.name = f"Node{nodeID}"
        self.position = (x, y)
        self.edges = []

    def getNeighbors(self):
        neighbors = []
        for edge in self.edges:
            if edge.isPassable:
                neighbors.append(edge.destNode)
        return neighbors

    def __eq__(self, other):
        return isinstance(other, Node) and self.nodeID == other.nodeID

    def __hash__(self):
        return hash(self.nodeID)

    def __lt__(self, other):
        return self.nodeID < other.nodeID