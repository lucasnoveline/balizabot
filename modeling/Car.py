import Pose2D


class Car():
    def __init__(self):
        self.pose = Pose2D.Pose2D(0, 0, 0)

    def update(self, vector):
        if vector is not None:
            self.pose = Pose2D.Pose2D(vector[0][0], vector[0][1], vector[1])