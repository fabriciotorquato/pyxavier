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
    if not os.path.isdir(os.path.expanduser("~/ros/catkin_ws/Results")):
        os.mkdir(os.path.expanduser("~/ros/catkin_ws/Results"))
    print("Digite o Nome da pessoa:")
    name = raw_input()
    if not os.path.isdir(os.path.expanduser("~/ros/catkin_ws/Results/"+name)):
        os.mkdir(os.path.expanduser("~/ros/catkin_ws/Results/"+name))
    date = datetime.datetime.now().strftime('%d-%m-%Y')
    if not os.path.isdir(os.path.expanduser("~/ros/catkin_ws/Results/"+name+"/"+date)):
        os.mkdir(os.path.expanduser("~/ros/catkin_ws/Results/"+name+"/"+date))
    print("Digite o nome do Metodo:")
    machineM = raw_input()   
    if not os.path.isdir(os.path.expanduser("~/ros/catkin_ws/Results/" + name + "/" + date + "/"+machineM)):
        os.mkdir(os.path.expanduser("~/ros/catkin_ws/Results/" + name + "/" + date + "/"+machineM))
    
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
            time = datetime.datetime.now().strftime("%H-%M-%S-%f")
            if not os.path.isdir(os.path.expanduser("~/ros/catkin_ws/Results/" + name +"/"+date + "/" + machineM + "/" + time)):
                os.mkdir(os.path.expanduser("~/ros/catkin_ws/Results/" + name +"/"+date + "/" + machineM + "/" + time))
            pubPath.publish(os.path.expanduser("~/ros/catkin_ws/Results/" + name +"/"+date + "/" + machineM + "/" + time))
            initi = False
            pub.publish(something)
            rate.sleep()
    

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
