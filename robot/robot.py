from robot.movement_controller import Movement_Controller
from robot.grasper_control import Grasper_Control

class Robot:
    def __init__(self, robotID):
        self.id = robotID
        self.position = (0, 0) # start position at warehouse, can change if we don't want to start at 0,0
        self.current_order = None
        self.status = "ready" # ready, busy, charging (if we implement charging stations later)
        self.movementController = Movement_Controller()
        self.grasper = Grasper_Control()

    def assignOrder(self, order):
        self.current_order = order
        self.status = "busy"

    def fufillOrder(self):
        # Foodie Bagger bags the items
        # robot should be given a series of bags in order
        # e.g. Robot.processBag
        return;

    def completeOrder(self):
        if self.position != self.current_order.getDestination():
            print("Error: robot not at destination, cannot complete order")
            return
        self.current_order = None
        self.status = "ready"
    
    def getStatus(self):
        return self.status
    
    def getID(self):
        return self.id