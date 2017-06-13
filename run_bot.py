from modeling.Modeling import Modeling
from control import LineFollower
from modeling import Pose2D
from modeling import Vector2
from communication import SendData
from decision_making import DecisionMaking

FORWARD = 1
BACKWARD = -1

model = Modeling()
model.init()

#control = LineFollower.LineFollower()
#communication = SendData.SendData()
decision_making = DecisionMaking.DecisionMaking()
decision_making.update(model)

model.update()
decision_making.update(model)
control.setControlData(model.car(), decision_making.desired_position, decision_making.line_ref)
dutyMotor1 = control.desiredVelocity()
dutyMotor2 = control.desiredVelocity()
servoAngle = control.desiredAngle()

direcao1 = FORWARD
direcao2 = FORWARD
communication.send(direcao1, direcao2, dutyMotor1, dutyMotor2, servoAngle)