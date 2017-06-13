import rospy
from std_msgs.msg import Float32MultiArray
import time

class SendData():
    def __init__(self):
        self.pub = rospy.Publisher('params_values',Float32MultiArray,queue_size = 10)
        rospy.init_node("SendData")
        self.r = rospy.Rate(10)

    def send(self, direcao1, direcao2, dutyMotor1, dutyMotor2, servoAngle):
        data = Float32MultiArray()
        data.data = [direcao1, direcao2, dutyMotor1, dutyMotor2, servoAngle]
        self.pub.publish(data)
