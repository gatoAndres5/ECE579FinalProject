class Destination:
    def __init__(self, destID, name, position):
        self.destID = destID
        self.name = name
        self.position = position
    
    def getCoords(self):
        return self.position