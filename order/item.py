class Item:
    def __init__(self, itemId, orderID, name, size, frozen, fragile):
        self.itemId = itemId
        self.orderID = orderID
        self.name = name
        self.size = size
        self.frozen = frozen
        self.fragile = fragile

    def isFrozen(self):
        return self.frozen
    
    def isFragile(self):
        return self.fragile
    
    def getSize(self):
        return self.size