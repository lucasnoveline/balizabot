from modeling.Modeling import Modeling
from control import LineFollower
from modeling import Pose2D
from modeling import Vector2
from communication import SendData
from decision_making import DecisionMaking
from time import sleep

FORWARD = 1
BACKWARD = -1

model = Modeling()

# VAI PEGAR AS LINHAS SIM
model.init()
model.init()
model.init()
model.init()
model.init()
model.init()
model.init()

#communication = SendData.SendData()
model.update()
decision_making = DecisionMaking.DecisionMaking()
decision_making.update(model)

control = LineFollower.LineFollower()
print 'extern line_ref = (%d, %d)' % (decision_making.line_ref.x, decision_making.line_ref.y)
control.setControlData(model.car, decision_making.desired_position, decision_making.line_ref)

dutyMotor1 = control.desiredVelocity()
dutyMotor2 = control.desiredVelocity()
servoAngle = control.desiredAngle()

direcao1 = FORWARD
direcao2 = FORWARD
communication.send(direcao1, direcao2, dutyMotor1, dutyMotor2, servoAngle)