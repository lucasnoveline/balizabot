class OtherCars:
    def __init__(self):
        self.cars = []
        self.quantity = []

    def update(self, vector):
        self.quantity = len(vector)
        for i in range(0, self.quantity/2, 1):
            self.cars[i].x = vector[i][0]
            self.cars[i].y = vector[i][1]
