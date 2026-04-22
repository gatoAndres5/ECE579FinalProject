class Robot:
    def __init__(self, robotID):
        self.id = robotID
        self.position = (0, 0) # start position at warehouse
        self.current_order = None
        self.status = "ready" # ready, busy, charging (if we implement charging stations later)
        # movement controller

    def assignOrder(self, order):
        self.current_order = order
        self.status = "busy"

    def completeOrder(self):
        self.current_order = None
        self.status = "ready"
    