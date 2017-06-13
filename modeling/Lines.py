class Lines:
    def __init__(self):
        self.lines = []
        self.quantity = 0

    def update(self, vector):
        # rectangles - [[centerx, centery],[height, width], angle of rotation]
        self.lines = []
        self.quantity = len(vector)
        for i in range(0, len(vector), 1):
            self.lines += [Line(vector[i][0][0], vector[i][0][1], vector[i][1][0], vector[i][1][1], vector[i][2])]


class Line:
    def __init__(self, x, y, height, width, rotation):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.rotation = rotation