# sshpass -p raspberry scp -r /home/grau/Documents/recognitionPi/raspberry/* pi@172.26.92.210:/home/pi/Documents
sshpass -p raspberry ssh pi@172.26.92.210 'rm -rf /home/pi/ros/catkin_ws/src/sender'
sshpass -p raspberry scp -r /home/lucasdutra/Desktop/TCC_Git/tcc-dtc-2019/ROS/sender/* pi@172.26.92.210:/home/pi/ros/catkin_ws/src/