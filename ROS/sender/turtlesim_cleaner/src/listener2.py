#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import xavier_command
from geometry_msgs.msg import Twist
import datetime

class TurtleBot:
	
	def __init__(self):
		self.vel_msg = Twist()
		self.speed = 3
		self.PI = 3.1415926535897
		self.angleT = 0
		self.init = False

	def callback(self, data):
		if self.init:
			car_publisher = rospy.Publisher('command', String, queue_size=10)
			decoy = self.toSpeed(data.data)
			car_publisher.publish(decoy)
			rospy.loginfo('%s - %s', data.data, decoy)
			
	def toSpeed(self,typeMove):
	    decodificado = ' '
	    if typeMove=='1':
				decodificado = xavier_command.FORWARD
		
	    elif typeMove=='0':
				decodificado = xavier_command.TURN_LEFT
	    elif typeMove == '2':
				decodificado = xavier_command.TURN_RIGHT

	    return decodificado
	
	def initListenet(self, data):
		if(data.data == "i" or data.data == "I"):
			self.init = True
		elif(data.data == "r" or data.data == "R"):
			car_publisher = rospy.Publisher('command', String, queue_size=10)
			decoy =  xavier_command.STOP
			car_publisher.publish(decoy)
			self.init = False
		elif(data.data == "p" or data.data == "P"):
			self.init = False
			car_publisher = rospy.Publisher('command', String, queue_size=10)
			decoy =  xavier_command.STOP
			car_publisher.publish(decoy)
		
	def listener(self):
		rospy.init_node('listener', anonymous=True)
		rospy.Subscriber('chatter', String, self.callback)
		rospy.Subscriber('letter', String, self.initListenet)
		rospy.spin()

if __name__ == '__main__':
    try:
	x = TurtleBot()
	x.listener()
	car_publisher = rospy.Publisher('command', String, queue_size=10)
	decoy =  xavier_command.STOP
	car_publisher.publish(decoy)
    except rospy.ROSInterruptException:
	car_publisher = rospy.Publisher('command', String, queue_size=10)
	decoy =  xavier_command.STOP
	car_publisher.publish(decoy)
        pass
