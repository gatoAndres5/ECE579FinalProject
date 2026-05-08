from robot.movement_controller import Movement_Controller
from robot.grasper_control import Grasper_Control
from bagging.bag import Bag
from routing.node import Node

class Robot:
    def __init__(self, fm, robotID, initial_location, environment_graph, true_obstacles):
        self.fm = fm
        self.id = robotID
        self.bags = []
        self.position = initial_location
        self.orders = []
        #self.currentOrder = None
        self.status = "ready"
        self.eg = environment_graph
        self.movementController = Movement_Controller(self, environment_graph, true_obstacles)
        self.grasper = Grasper_Control(self) 
        self.maxCapacity = 6 # max number of bags
        self.movementStatus = None
        self.battery = 100 # start fully charged
        self.dispatchTicks = 0 # for when orders are not given simultaneously
        self.dispatchTimeout = 5 # timeout and dispatch after waiting this period

    def assignOrder(self, order):
        self.orders.append(order)
        if self.status == "ready":
            self.status = "assigned"
            self.dispatchTicks = 0

    def setDestination(self, destination):
        self.movementController.setDestination(destination)

    def getCurrentOrder(self):
        return self.movementController.currentTargetOrder;

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
        #self.currentOrder = None

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
        # battery drains by drain_rate% per distance travelled
        drain_rate = 1
        self.battery -= distance * drain_rate

    def chargeBattery(self, percent):
        self.battery += percent

    def getBattery(self):
        return self.battery
    
    def tick(self):
        if self.status == "busy":
            movementStatus = self.movementController.step()
            self.movementStatus = movementStatus
            self.drainBattery(1)

            if movementStatus == "COMPLETE":
                # arrived at destination
                currOrder = self.movementController.currentTargetOrder

                if currOrder and self.position == currOrder.getDestination():
                    print(f"Robot {self.id}: movement complete to {self.position.name}.")
                    self.removeAllBags(self.movementController.destinationNode, currOrder)
                    # target the next destination
                    self.movementController.targetNextDestination()
                elif self.position == self.fm.fw:
                    # returned to FW
                    print(f"Robot {self.id}: returned to FW")
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

        elif self.status == "ready":
            print(f"Robot {self.id}: ready")

        elif self.status == "charging":
            print(f"Robot {self.id}: charging ({self.battery}%)")
            self.chargeBattery(5)
            if self.battery >= 100:
                self.status = "ready"

        elif self.status == "assigned":
            print(f"Robot {self.id}: waiting for more orders"
                  f"({self.dispatchTicks}/{self.dispatchTimeout})")
            self.dispatchTicks += 1
            
            # if compartment at capacity, dispatch
            if len(self.bags) >= self.maxCapacity:
                self.dispatch()
            # if past timeout, dispatch
            elif self.dispatchTicks >= self.dispatchTimeout:
                self.dispatch()

    def dispatch(self):
        if not self.orders:
            print(f"Error: Robot {self.id} cannot dispatch with no order")

        self.movementController.setItinerary(self.orders)
        self.status = "busy"
        self.dispatchTicks = 0

        print(f"Robot {self.id}: dispatched with {len(self.orders)} order(s)")