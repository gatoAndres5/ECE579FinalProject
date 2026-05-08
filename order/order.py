from datetime import datetime

class Order:
    def __init__(self, orderId, destination, items=None):
        self.orderId = orderId
        self.destination = destination
        self.status = "WAITING"
        if items:
            self.items = items
        else:
            self.items = []
        self.orderTime = datetime.now()
    
    def getStatus(self):
        return self.status
    
    def getItems(self):
        return self.items
    
    def getDestination(self):
        return self.destination
    
    def updateStatus(self, newStatus):
        self.status = newStatus
