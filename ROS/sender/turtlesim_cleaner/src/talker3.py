#!/usr/bin/env python
import rospy
import requests
from std_msgs.msg import String
import numpy as np        
import pandas as pd  
import random
import socket
import time

def talker():
    val = random.randint(0,2)
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10)   
    while not rospy.is_shutdown():
        pub.publish(str(val))
	if random.randint(0,101)<=20:
		val = random.randint(0,2)
        time.sleep(0.250)
	
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
