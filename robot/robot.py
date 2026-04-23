from robot.movement_controller import Movement_Controller
from robot.grasper_control import Grasper_Control
from bagging.bag import Bag

class Robot:
    def __init__(self, robotID):
        self.id = robotID
        self.bags = []
        self.position = (0, 0) # start position at warehouse, can change if we don't want to start at 0,0
        self.currentOrder = None
        self.status = "ready" # ready, busy, charging (if we implement charging stations later)
        self.movementController = Movement_Controller(self)
        self.grasper = Grasper_Control(self) 
        self.maxCapacity = 6 # max number of bags

    def assignOrder(self, order):
        self.currentOrder = order
        self.status = "busy"

    def getCurrentOrder(self):
        return self.currentOrder;

    def addBag(self, bag, location):
        if (len(self.bags) >= self.maxCapacity):
            print(f"Error: no room to add another bag.")
            return;
        self.grasper.pickUp(bag, location)
        self.grasper.putDown(bag, self.position)
        self.bags.append(bag);
        print(f"Robot {self.id}: added bag {bag.getID()}")

    def removeBag(self, bag, location):
        # TODO fix location and decide relative or absolute
        self.grasper.pickUp(bag, self.position)
        self.grasper.putDown(bag, location)
        self.bags.remove(bag)


    def removeAll(self, location):
        # remove all bags, placing at location
        for b in self.bags:
            self.removeBag(b, location);

    def completeOrder(self):
        if self.position != self.currentOrder.getDestination():
            print("Error: robot not at destination, cannot complete order")
            return
        self.currentOrder = None
        self.status = "ready"
    
    def getStatus(self):
        return self.status
    
    def getID(self):
        return self.id