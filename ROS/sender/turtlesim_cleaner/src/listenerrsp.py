#!/usr/bin/env python
import rospy
import xavier_command
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class TurtleBot:


        def callback(self, data):
                print(data)

        def listener(self):
                print(xavier_command.FORWARD)
                rospy.init_node('meuComputador', anonymous=True)
                rospy.Subscriber('letterX', String, self.callback)
                rospy.spin()

if __name__ == '__main__':
    x = TurtleBot()
    x.listener()
	


