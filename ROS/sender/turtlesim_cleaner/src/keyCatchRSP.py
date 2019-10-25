#!/usr/bin/env python
import rospy
import requests
from std_msgs.msg import String
import random
from geometry_msgs.msg import Twist

def talker():
    initi = True
    pub = rospy.Publisher('command', String, queue_size=10)
    rospy.init_node('letterTalkerS', anonymous=True)
    rate = rospy.Rate(1) # 1hz
    while not rospy.is_shutdown():
	    something = raw_input()
            pub.publish(something)
            rate.sleep()
    

if __name__ == '__main__':
    try:
        talker()
	car_publisher = rospy.Publisher('command', String, queue_size=10)
	decoy =  xavier_command.STOP
	car_publisher.publish(decoy)
    except rospy.ROSInterruptException:
	car_publisher = rospy.Publisher('command', String, queue_size=10)
	decoy =  xavier_command.STOP
	car_publisher.publish(decoy)
        pass

