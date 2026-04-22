class Grasper_Control:
    def __init__(self, robot):
        self.robot = robot
        self.open = False
        self.position = (0, 0)
        self.handEmpty = True
        self.itemHeld = None

    def pickUp(self, item, itemPosition):
        if (not self.handEmpty):
            print("Error: hand not empty")
            return
        self.moveTo(itemPosition)
        self.closeGrasper()
        self.itemHeld = item
        self.handEmpty = False

    def putDown(self, bagPosition):
        if (self.handEmpty):
            print("Error: hand empty")
            return
        self.moveTo(bagPosition)
        self.openGrasper()
        self.itemHeld = None
        self.handEmpty = True

    def moveTo(self, new_position):
        self.position = new_position

    def openGrasper(self):
        self.open = True

    def closeGrasper(self):
        self.open = False

