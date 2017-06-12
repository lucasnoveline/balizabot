class Lines:
    def __init__(self):
        self.lines = []
        self.lines.x = []
        self.lines.y = []
        self.lines.height = []
        self.lines.width = []
        self.lines.rotation = []

    def update(self, vector):
        # rectangles - [[centerx, centery],[height, width], angle of rotation]
        for i in range(0, len(vector), 1):
            self.lines[i].x = vector[i][0]
            self.lines[i].y = vector[i][1]
            self.lines[i].height = vector[i][2]
            self.lines[i].width = vector[i][3]
            self.lines[i].rotation = vector[i][4]
