from modeling import Pose2D

class DecisionMaking:
    def __init__(self):
        self.desired_position = []
        self.line_ref = []
        self.vagasDisponiveis = 0

    def update(self, model):
