from bagging.item import Item
from routing.node import Node

class Bag:
    def __init__(self, bagID, initial_location, order, bagType="paper", capacity=10):
        self.bagID = bagID
        self.name = f"Bag {bagID}"
        self.bagType = bagType  # either "paper" or "freezer"
        self.items = []
        self.order = order
        self.current_weight = 0
        self.capacity = capacity
        self.location = initial_location

        self.contains_fragile = False
        self.contains_heavy = False

    def can_fit(self, item):
        if self.current_weight + item.getWeight() > self.capacity:
            return False
        if (item.isFrozen() and self.bagType != "freezer") or (not item.isFrozen() and self.bagType == "freezer"):
            return False
            
        if item.isFragile() and self.contains_heavy:
            return False
        if self.contains_fragile and item.isHeavy():
            return False
            
        return True

    def addItem(self, item):
        self.items.append(item)
        self.current_weight += item.getWeight()
        if item.isFragile():
            self.contains_fragile = True
        if item.isHeavy():
            self.contains_heavy = True

    def getItems(self):
        return self.items

    def getID(self):
        return self.bagID

    def getName(self):
        return self.name

    def getLocation(self):
        return self.location

    def getOrder(self):
        return self.order
    
    def getBagType(self):
        return self.bagType