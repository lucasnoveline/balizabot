import Car
import OtherCars
import Vacancy
from vision import vision
from vision import camera
from math import tan
import Lines

DEBUG = False
if DEBUG:
    import cv2


class Modeling:
    def __init__(self):
        self.vis = vision.Vision()
        self.cam = camera.Camera()
        self.lines = Lines.Lines()
        self.car = Car.Car()
        self.other_cars = OtherCars.OtherCars()
        self.vacancies = None
        self.frame = None

    def init(self):
        self.frame = self.cam.getFrame()
        frame = self.frame

        lines = self.vis.detect_lines(frame)
        other_cars = self.vis.detect_other_cars(frame)
        self.other_cars.update(other_cars)
        self.lines.update(lines)

        #get vacancies
        self.vacancies = Vacancy.Vacancies(self.other_cars, self.lines)

    def update(self):
        self.frame = self.cam.getFrame()
        frame = self.frame

        car = self.vis.detect_car(frame)
        self.car.update(car)

        if DEBUG:
            # draw vacancies
            for vacancy in self.vacancies.vacancies:
                cv2.circle(frame, (int(vacancy.center.x), int(vacancy.center.y)), 4, (255, 0, 0), 3)
            # draw other cars
            for other_car in self.other_cars.cars:
                cv2.circle(frame, (int(other_car.x), int(other_car.y)), 4, (0, 255, 0), 3)
            # draw car direction
            cv2.circle(frame, (int(self.car.pose.x), int(self.car.pose.y)), 4, (0, 0, 255), 3)
            cv2.circle(frame, (int(self.car.pose.x - 20),
                               int(self.car.pose.y - 20 * tan(self.car.pose.rotation))), 4, (0, 0, 255), 3)

            cv2.imshow('debug', frame)
            cv2.waitKey(1)