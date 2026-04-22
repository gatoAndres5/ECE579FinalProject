from obstacle.obstacle_detection import ObstacleDetection

class Movement_Controller:
    def __init__(self, robot):
        self.robot = robot
        self.obstacleDetector = ObstacleDetection()

    # movement along an edge
    # 