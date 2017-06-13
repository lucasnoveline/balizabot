import rospy
from std_msgs.msg import Float32MultiArray
import time

pub = rospy.Publisher('params_values',Float32MultiArray,queue_size = 10)
rospy.init_node("values_publisher")

r= rospy.Rate(10)
while not rospy.is_shutdown():
    a = Float32MultiArray()
    # for x in range (100):
	# a.data = [x*0.1+10]
	# pub.publish(a)
	# print x*0.1+10
	# time.sleep(0.2)
    # for x in range (100):
	# a.data = [20-x*0.1]
	# pub.publish(a)
	# print 20-0.1*x
	# time.sleep(0.2)
	#a.data = [direcao, velocidade, angulo]
    a.data = [0,1,3.3]
    pub.publish(a)
    # r.sleep()


