import Vector2
DEBUG = False

class OtherCars:
    def __init__(self):
        self.cars = []
        self.quantity = 0

    def update(self, vector):
        self.quantity = len(vector)
        for i in range(0, self.quantity):
            if DEBUG:
                print 'other car %d: (%d,%d)' % (i, vector[i][0], vector[i][1])
            self.cars += [Vector2.Vector2(vector[i][0], vector[i][1])]