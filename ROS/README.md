# Ros
## Install ROS

* [ROS](http://wiki.ros.org/kinetic/Installation)


## Library

### Python

* sudo pip install numpy scipy
* sudo pip install pandas
* sudo pip install -U scikit-learn

### ROS
 * roscore 
 * sudo apt-get install ros-indigo-turtlesim 
 

 
## Criar o workplace
* mkdir -p ~/ros/catkin_ws/src
* cd ~/ros/catkin_ws
* catkin_make
* colar a pasta turtlesim_cleaner ~/ros/catkin_ws/src

## Run
    in script knnTalker configure the path for the computer
    
    open the first terminal and start the ROS
    roscore
    
    open the second terminal and start the turtle
    rosrun turtlesim turtlesim_node
    
    open the third terminal and start the KNN
    cd ros/catkin_ws
    source devel/setup.bash
    rosrun turtlesim_cleaner knnTalker.py
    
    open the terminal room and start the listener
    cd ros/catkin_ws
    source devel/setup.bash
    rosrun turtlesim_cleaner listener.py

    
