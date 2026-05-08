
class Grasper_Control:
    def __init__(self, robot): 
        self.robot = robot
        self.open = True
        self.position = (0, 0) # not a Node
        self.handEmpty = True
        self.itemHeld = None

    def pickUp(self, item, itemPosition):
        if (not self.handEmpty):
            print("Error: hand not empty")
            return
        #if (item.getPosition() != itemPosition):
        #    print("Error: item not at expected location");
        self.moveTo(itemPosition)
        self.closeGrasper()
        self.itemHeld = item
        self.handEmpty = False

        print(f"Robot {self.robot.getID()}: picked up {item.getName()}")

    def putDown(self, destination):
        if (self.handEmpty):
            print("Error: hand empty")
            return
        self.moveTo(destination)
        self.openGrasper()
        self.itemHeld = None
        self.handEmpty = True

    def moveTo(self, new_position):
        self.position = new_position

    def openGrasper(self):
        self.open = True

    def closeGrasper(self):
        self.open = False

    def isOpen(self):
        return self.open
    
    def getItemHeld(self):
        return self.itemHeld;