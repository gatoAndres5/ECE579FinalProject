class Grasper_Control:
    def __init__(self, robot):
        self.robot = robot
        self.open = False
        self.position = (0, 0)
        self.handEmpty = True

    def pickUp(self, item_position):
        if (not self.handEmpty):
            print("Error, hand not empty")
            return
        self.position = item_position # move
        self.closeGrasper() # grasp item
        self.handEmpty = False

    def openGrasper(self):
        self.open = True

    def closeGrasper(self):
        self.open = False

