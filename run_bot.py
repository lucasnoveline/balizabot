from modeling import Modeling
from control import LineFollower
from modeling import Pose2D
from modeling import Vector2
from communication import SendData

if __name__ == "__main__":
    model = Modeling()
    control = LineFollower()
    communication = SendData()
    frente = 1
    tras = -1
    model.update()

    # Aqui vem o decision_making
    desired_position = Pose2D()
    line_ref = Vector2()
    control.SetControlData(model.car(), desired_position, line_ref)
    dutyMotor1 = control.DesiredVelocity()
    dutyMotor2 = control.DesiredVelocity()
    servoAngle = control.DesiredAngle()
    direcao1 = frente
    direcao2 = frente
    communication.Send(direcao1, direcao2, dutyMotor1, dutyMotor2, servoAngle)