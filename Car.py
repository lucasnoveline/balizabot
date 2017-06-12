class Car():
    def __init__(self):
        self.x = []
        self.y = []
        self.rotation = []

    def update(self, vector):
        self.x = vector(1)
        self.y = vector(2)
        self.rotation = vector(3)

