from modeling import Vector2

class Vacancy:
    def __init__(self, otherCars, lineUp, lineDown, state):
        self.lineUp = lineUp
        self.lineDown = lineDown
        self.center = Vector2((lineUp.x + lineDown.x)/2, (lineUp.y + lineDown.y)/2)
        self.state = False
        for i in range(0, otherCars.quantity, 1):
            if otherCars.cars[i].y < lineUp.y & otherCars.cars[i].y > lineDown.y:
                self.state = True
