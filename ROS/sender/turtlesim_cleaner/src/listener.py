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
			distance = 1
			velocity_publisher = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) 
			car_publisher = rospy.Publisher('command', String, queue_size=10)
			decoy = self.toSpeed(data.data)
			car_publisher.publish(decoy)
			rospy.loginfo('%s - %s', data.data, decoy)
			rospy.loginfo(self.angleT)
			#rospy.loginfo(angle)
			t0 = rospy.Time.now().to_sec()
			current_distance = 0
			while(current_distance < distance):
				#Publish the velocity
				velocity_publisher.publish(self.vel_msg)
				#Takes actual time to velocity calculus
				t1=rospy.Time.now().to_sec()
				#Calculates distancePoseStamped
				current_distance= self.speed*(t1-t0)
				#After the loop, stops the robot
				self.toSpeed('reset')
				#Force the robot to stop
				velocity_publisher.publish(self.vel_msg)

	def toSpeed(self,typeMove):
	    decodificado = ' '
	    if typeMove=='1':
				self.vel_msg.linear.y = 0
				self.vel_msg.linear.z = 0
				self.vel_msg.angular.x = 0
				self.vel_msg.angular.y = 0	
				self.vel_msg.angular.z = 0
				self.vel_msg.linear.x =  1
				decodificado = xavier_command.FORWARD
		
	    elif typeMove=='0':
				self.vel_msg.linear.y = 0
				self.vel_msg.linear.z = 0
				self.vel_msg.angular.x = 0
				self.vel_msg.angular.y = 0	
				self.vel_msg.angular.z = 1
				self.vel_msg.linear.x =  1
				decodificado = xavier_command.TURN_LEFT
	    elif typeMove == '2':
				self.vel_msg.linear.y = 0
				self.vel_msg.linear.z = 0
				self.vel_msg.angular.x = 0
				self.vel_msg.angular.y = 0	
				self.vel_msg.angular.z = -1
				self.vel_msg.linear.x =  1
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


