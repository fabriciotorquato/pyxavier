#!/usr/bin/env python
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from xavier_car_tester import XavierCar
class TurtleBot:
	
	def __init__(self):
		self.xavier_car = XavierCar()
		self.xavier_car.start_avoidance()
	
	def listener(self):

		rospy.init_node('picar_controller', anonymous=True)
		rospy.Subscriber('command', String, self.xavier_car.send_command)
		rospy.spin()
	
	def stop(self):
		self.xavier_car.stop()

if __name__ == '__main__':
	turtleBot = TurtleBot()	
	try:				
		turtleBot.listener()
	except:
		turtleBot.stop()
