#!/usr/bin/env python
import rospy
import requests
from std_msgs.msg import String
import numpy as np        
import pandas as pd  
import random
import socket

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(5)   
    HOST = ''              
    PORT = 5000           
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)
    while not rospy.is_shutdown():
        con, cliente = tcp.accept()
        msg = con.recv(1024)
        rospy.loginfo(msg)
        pub.publish(msg)
        rate.sleep()
    con.close()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
