from bagging.item import Item

class Bag:
    def __init__(self, bagID, bagType="paper", capacity=10):
        # can adjust capacity of 10 as well
        self.bagID = bagID
        self.name = f"Bag{bagID}"
        self.bagType = bagType  # either "paper" or "freezer"
        self.items = []
        self.current_weight = 0
        self.capacity = capacity

        self.contains_fragile = False
        self.contains_heavy = False

    def can_fit(self, item):
        if self.current_weight + item.getWeight() > self.capacity:
            return False
        if (item.isFrozen() and self.bagType != "freezer") or (not item.isFrozen() and self.bagType == "freezer"):
            return False
            
        if item.isFragile() and self.contains_heavy:
            return False
        if self.contains_fragile and item.getSize() == 'large':
            return False
            
        return True

    def addItem(self, item):
        self.items.append(item)
        self.current_weight += item.getWeight()
        if item.isFragile():
            self.contains_fragile = True
        if item.getSize() == 'large':
            self.contains_heavy = True