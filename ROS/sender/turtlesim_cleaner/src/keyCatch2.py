#!/usr/bin/env python
import rospy
import requests
from std_msgs.msg import String
import random
from geometry_msgs.msg import Twist
import os
import datetime

def talker():
    initi = True
    pub = rospy.Publisher('letter', String, queue_size=10)
    pubPath = rospy.Publisher('folderPath', String, queue_size=900)
    rospy.init_node('letterTalker', anonymous=True)
    rate = rospy.Rate(1) # 1hz

    while not rospy.is_shutdown():
        if initi:
            print("Precione I para iniciar")
        else:
            print("Precione R para reiniciar a simulacao")
        something = raw_input()
        if (something == "r" or something == "R") and not initi:
            initi = True
            pub.publish(something)
            rate.sleep()

        elif (something == "i" or something == "I") and initi:
            initi = False
            pub.publish(something)
            rate.sleep()
    

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
