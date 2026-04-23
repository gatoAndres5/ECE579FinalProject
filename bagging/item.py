class Item:
    def __init__(self, itemID, name, size, frozen=False, fragile=False):
        self.itemID = itemID
        self.name = f"{name}_{itemID}"
        self.size = size  # string: 'large', 'medium', 'small'
        self.frozen = frozen 
        self.fragile = fragile

    def getWeight(self):
        # can adjust weights later if needed
        if self.size == 'large': return 5
        if self.size == 'medium': return 3
        if self.size == 'small': return 1
        return 0

    def isFrozen(self):
        return self.frozen

    def isFragile(self):
        return self.fragile

    def getSize(self):
        return self.size
    
    def getName(self):
        return self.name
    
    def getID(self):
        return self.itemID