class OtherCars:
    def __init__(self):
        self.cars = []

    def update(self, vector):
        n = len(vector)
        for i in range(0, n/2, 1):
            self.cars[i].x = vector[i][0]
            self.cars[i].y = vector[i][1]
