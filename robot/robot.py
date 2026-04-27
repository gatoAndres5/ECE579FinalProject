from robot.movement_controller import Movement_Controller
from robot.grasper_control import Grasper_Control
from bagging.bag import Bag
from routing.node import Node

class Robot:
    def __init__(self, fm, robotID, initial_location, environment_graph, true_obstacles):
        self.fm = fm
        self.id = robotID
        self.bags = []
        self.position = initial_location # start position at warehouse, can change if we don't want to start at 0,0
        self.currentOrder = None
        self.status = "ready" # ready, busy, charging (if we implement charging stations later)
        self.eg = environment_graph
        self.movementController = Movement_Controller(self, environment_graph, true_obstacles)
        self.grasper = Grasper_Control(self) 
        self.maxCapacity = 6 # max number of bags
        self.movementStatus = None
        self.battery = 100 # start fully charged

    def assignOrder(self, order):
        self.currentOrder = order
        self.status = "busy"

    def setDestination(self, destination):
        self.movementController.setDestination(destination)

    def getCurrentOrder(self):
        return self.currentOrder;

    def addBag(self, bag, location):
        if (len(self.bags) >= self.maxCapacity):
            print(f"Error: no room to add another bag.")
            return;
        self.grasper.pickUp(bag, location)
        self.grasper.putDown(self.position)
        self.bags.append(bag);
        print(f"Robot {self.id}: added bag {bag.getID()}")

    def removeBag(self, bag, location):
        self.grasper.pickUp(bag, self.position)
        self.grasper.putDown(location)
        self.bags.remove(bag)

    def removeAllBags(self, location, order=None):
        # remove all bags, placing at location
        if order is not None:
            for b in self.bags:
                if b.order == order:
                    self.removeBag(b, location)
    
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
    
    def getCapacity(self):
        return self.maxCapacity
    
    def getPosition(self):
        return self.position
    
    def drainBattery(self, distance):
        # battery drains by 1% per distance travelled
        self.battery -= distance

    def chargeBattery(self, percent):
        self.battery += percent

    def getBattery(self):
        return self.battery
    
    def tick(self):
        if self.status == "busy":
            movementStatus = self.movementController.step()
            self.drainBattery(1)
            self.movementStatus = movementStatus

            if movementStatus == "COMPLETE": #and self.position == self.currentOrder.getDestination():
                # arrived at destination
                print(f"Robot {self.id}: movement complete. Returning to FW.")
                self.removeAllBags(self.movementController.destinationNode)

                if self.position == self.currentOrder.getDestination():
                    self.movementController.setDestination(self.fm.fw) # send robot back to FW
                elif self.position == self.fm.fw:
                    self.fm.completeOrder(self.id) # notify FleetManager order is complete
                    self.status = 'ready'
            elif movementStatus == "FAIL":
                self.status = "error"
                print(f"Error: robot {self.id} in an error state.")
            elif movementStatus == "MOVING":
                return # do nothing
        elif self.status == 'ready':
            print(f"Robot {self.id}: ready")

        elif self.status == 'charging':
            print(f"Robot {self.id}: charging")
            self.chargeBattery(1)