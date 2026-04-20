class OrderManager:
    def __init__(self, pendingOrders, activeOrders, completedOrders):
        if pendingOrders:
            self.pendingOrders = pendingOrders
        else:
            self.pendingOrders = []
        
        if activeOrders:
            self.activeOrders = activeOrders
        else:
            self.activeOrders = []
        
        if completedOrders:
            self.completedOrders = completedOrders
        else:
            self.completedOrders = []
    
    def getNextOrder(self):
        if not self.pendingOrders:
            return None
        return self.pendingOrders[0]

    
    def dispatchOrder(self):
        if not self.pendingOrders:
            return None

        order = self.pendingOrders.pop(0)
        order.updateStatus("ASSIGNED")
        self.activeOrders.append(order)

        return order

    def markComplete(self, order):
        if order in self.activeOrders:
            self.activeOrders.remove(order)
            order.updateStatus("DELIVERED")
            self.completedOrders.append(order)
