#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from xavier_car import XavierCar
class TurtleBot:
	
	def __init__(self):
		self.xavier_car = XavierCar()
		self.xavier_car.start_avoidance()
	
	def listener(self):

		rospy.init_node('picar_controller', anonymous=True)
		rospy.Subscriber('command', String, self.xavier_car.send_command)
		rospy.spin()

if __name__ == '__main__':
    x = TurtleBot()
    x.listener()
