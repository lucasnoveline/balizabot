from modeling import Pose2D, Vector2
from math import atan2
import cv2

OFFSET = 100
DEBUG = True

class DecisionMaking:
    def __init__(self):
        self.desired_position = Pose2D.Pose2D(0,0,0)
        self.line_ref = Vector2.Vector2(0,0)

    def update(self, model):
        #ver se tem vagas disponiveis e escolher uma delas
        chosen_vacancy = None
        size = 0

        if DEBUG is True:
            print 'number of vacancies = %d' % len(model.vacancies.vacancies)
        for vacancy in model.vacancies.vacancies:
            if DEBUG is True:
                print 'size = %d' % (vacancy.line_up.x - vacancy.line_down.x)
            if size < (vacancy.line_up.x - vacancy.line_down.x):
                chosen_vacancy = vacancy
                size = (vacancy.line_up.x - vacancy.line_down.x)
        if chosen_vacancy is None:
            return

        #determinar a posicao desejada
        self.desired_position.x = chosen_vacancy.line_up.x
        self.desired_position.y = chosen_vacancy.line_up.y + OFFSET
        self.desired_position.rotation = atan2(chosen_vacancy.line_up.y - chosen_vacancy.line_down.y,
                                               chosen_vacancy.line_up.x - chosen_vacancy.line_down.x)

        self.line_ref = Vector2.Vector2(chosen_vacancy.line_up.y - chosen_vacancy.line_down.y,
                                        chosen_vacancy.line_up.x - chosen_vacancy.line_down.x)

        if DEBUG is True:
            print 'line_ref: (%d, %d)' % (self.line_ref.x, self.line_ref.y)

            frame = model.frame
            cv2.circle(frame, (int(self.desired_position.x), int(self.desired_position.y)), 4, (0, 255, 0), 3)
            cv2.imshow('desired position debug', frame)
            cv2.waitKey(1)
