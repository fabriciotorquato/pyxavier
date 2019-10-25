#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
import geometry_msgs.msg
import turtlesim.srv
import std_srvs.srv
from std_srvs.srv import Empty
from std_msgs.msg import String
import time
import numpy
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import random
from app_screenshot import App

class SpawnerTurtle:
   def __init__(self):
      self.pub = rospy.Publisher('letter', String, queue_size=10)
      self.state = False
      self.timeInit = time.time()
      self.timeEnd = time.time()
      self.pose1 = Pose()
      self.pose2 = Pose()
      self.finalState = False
      self.folderPath = ''
   def randomSpaw(self, data):
      
      if(data.data == "i" or data.data == "I"):
         random.seed()
         rospy.wait_for_service('spawn')
         spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
         self.pose2 = Pose()
         if random.randint(1,10) % 2 == 0:
            random.seed()
            self.pose2.x =  random.uniform(0.3, 3.9)
         else:
            random.seed()
            self.pose2.x =  random.uniform(8.0, 11.0)

         if random.randint(1,10) % 2 == 0:
            random.seed()
            self.pose2.y =  random.uniform(0.3, 3.9)
         else:
            random.seed()
            self.pose2.y =  random.uniform(8.0, 11.0)
         spawner(self.pose2.x, self.pose2.y, 0, 'turtle2')
         self.state = True
         self.timeInit = time.time()
         self.pose1 = Pose()
         self.pose1.x = -150
         self.pose1.y = -150

      elif(data.data == "r" or data.data == "R"):
         if not self.finalState:
            timeTotal = time.time() - self.timeInit
            print("Tempo decorrido:",timeTotal)
            f = open(self.folderPath+'/resultados.txt','w')
            f.write('Status: Incompleto\r\nTempo: '+str(timeTotal))
            f.close()
            screenShot = App()
            screenShot.screenshot(self.folderPath,"imagem")
            self.state = False
            self.pub.publish("P")
         self.finalState = False
         rospy.wait_for_service('reset')
         reset = rospy.ServiceProxy('reset', Empty)
         reset()



   def attTurtle1(self, data):
      self.pose1.x = data.x
      self.pose1.y = data.y


   def chceckPosition(self):
      if self.state:
         if(self.pose2.x - 1.0 <= self.pose1.x and self.pose1.x <= self.pose2.x + 1.0 
         and self.pose2.y - 1.0 <= self.pose1.y and self.pose1.y <= self.pose2.y + 1.0):
            timeTotal = time.time() - self.timeInit
            print("Tempo que levou para chegar:",timeTotal)
            f = open(self.folderPath+'/resultados.txt','w')
            f.write('Status: Completo\r\nTempo: '+str(timeTotal))
            f.close()
            screenShot = App()
            screenShot.screenshot(self.folderPath,"imagem")
            self.pub.publish("P")
            self.state = False
            self.finalState = True

   def updatePath(self, data):
      self.folderPath = data.data

   def listener(self):
      rospy.init_node('spawner', anonymous=True)  
      rate = rospy.Rate(10.0)
      rospy.Subscriber('folderPath', String, self.updatePath)
      rospy.Subscriber('letter', String, self.randomSpaw)
      rospy.Subscriber('/turtle1/pose',Pose, self.attTurtle1)
      while not rospy.is_shutdown():
         self.chceckPosition()
      rospy.spin()
      
   
if __name__ == '__main__':
   x = SpawnerTurtle()
   x.listener()
   
