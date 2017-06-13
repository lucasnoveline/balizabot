#!/usr/bin/env python


import rospy
from std_msgs.msg import Float32MultiArray

def callbackFloatReceiver(data):
    print data.data[0],data.data[1]


rospy.init_node('float_receiver',anonymous=True)
rospy.Subscriber("params_values",Float32MultiArray,callbackFloatReceiver)
while not (rospy.is_shutdown()):
    rospy.spin()
