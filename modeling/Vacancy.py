from modeling import Vector2
DEBUG = False

class Vacancies:
    def __init__(self, other_cars, lines):
        # get all lines, sorted by y
        sorted_lines = sorted(lines.lines, key=lambda line: line.x)
        self.quantity = len(sorted_lines) - 1
        self.vacancies = []
        for i in range(0, len(sorted_lines)-1):
            line_up = sorted_lines[i+1]
            line_down = sorted_lines[i]

            # check if car is in place
            busy = False
            if DEBUG:
                print 'line up: (%d, %d) line down (%d, %d)' % (line_up.x, line_up.y, line_down.x, line_down.y)
            for j in range(0, other_cars.quantity):
                if DEBUG:
                    print '\t car %d: (%d, %d)' % (j, other_cars.cars[j].x, other_cars.cars[j].y)
                if line_up.x > other_cars.cars[j].x > line_down.x:
                    busy = True
            if not busy:
                self.vacancies += [Vacancy(line_up, line_down)]


class Vacancy:
    def __init__(self, line_up, line_down):
        self.line_up = line_up
        self.line_down = line_down
        self.center = Vector2.Vector2((self.line_up.x + self.line_down.x) / 2, (self.line_up.y + self.line_down.y) / 2)