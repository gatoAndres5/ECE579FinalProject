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
        print(f"Robot {self.id}: added {bag.getID()} to inventory")

    def removeBag(self, bag, location):
        self.grasper.pickUp(bag, self.position)
        self.grasper.putDown(location)
        self.bags.remove(bag)
        print(f"Robot {self.id}: removed {bag.getName()} from inventory")

    def removeAllBags(self, location, order=None):
        # if an order is specified, remove only those bags
        for b in self.bags[:]:
            if order:
                if b.order == order:
                    self.removeBag(b, location)
            else:
                self.removeBag(b, location)
        return

    def completeOrder(self):
        self.currentOrder = None

        if self.battery < 30:
            print(f"Robot {self.id} began charging.")
            self.status = "charging"
        else:
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
            self.movementStatus = movementStatus
            self.drainBattery(1)

            if movementStatus == "COMPLETE": #and self.position == self.currentOrder.getDestination():
                # arrived at destination
                currOrder = self.movementController.currentTargetOrder

                if currOrder and self.position == currOrder.getDestination():
                    print(f"Robot {self.id}: movement complete to {self.position.name}.")
                    self.removeAllBags(self.movementController.destinationNode, currOrder)

                    # target the next destination
                    self.movementController.targetNextDestination()
                elif self.position == self.fm.fw:
                    # returned to FW
                    print(f"Robot {self.id} returned to FW")
                    self.fm.completeOrder(self.id) # notify FleetManager order is complete
                else:
                    self.removeAllBags(self.movementController.destinationNode)
                    self.movementController.targetNextDestination()
                    
            elif movementStatus == "FAIL":
                self.status = "error"
                print(f"Error: robot {self.id} in an error state.")
            elif movementStatus == "MOVING":
                if self.battery <= 0:
                    print(f"Error: robot {self.id} battery died.")
                    self.status = "dead"
                return # do nothing
            
        elif self.status == "ready":
            print(f"Robot {self.id}: ready")

        elif self.status == "charging":
            print(f"Robot {self.id}: charging ({self.battery}%)")
            self.chargeBattery(5)
            if self.battery >= 100:
                self.status = "ready"

