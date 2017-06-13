import Car
import OtherCars
import vision.camera

import vision
from modeling import Lines


class Modeling:
    def __init__(self):
        self.vis = vision.Vision()
        self.cam = vision.camera.Camera()
        self.lines = Lines.Lines
        self.car = []
        self.otherCars = []
        self.car = Car()
        self.otherCars = OtherCars()
        self.lines = Lines()

    def update(self):
        frame = self.cam.getFrame()
        lines = self.vis.detect_lines(frame)
        car = self.vis.detect_car(frame)
        other_cars = self.vis.detect_other_cars(frame)
        self.lines.update(lines)
        self.car.update(car)
        self.otherCars.update(other_cars)
