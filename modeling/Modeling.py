import Car
import OtherCars
import camera

import vision
from modeling import Lines


class Modeling:
    def __init__(self):
        self.vis = vision.Vision()
        self.cam = camera.Camera()
        self.lines = Lines.Lines
        self.car = []
        self.otherCars = []
        self.car = Car()
        self.otherCars = OtherCars()
        self.lines = Lines()

    def init(self):
        frame = self.cam.getFrame()
        lines = self.vis.detect_lines(frame)
        other_cars = self.vis.detect_other_cars(frame)
        self.otherCars.update(other_cars)
        self.lines.update(lines)

    def update(self):
        frame = self.cam.getFrame()
        car = self.vis.detect_car(frame)
        self.car.update(car)
