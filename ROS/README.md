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
    no script knnTalker configurar o path para o do cumputador 
    
    abra o primeiro terminal e inicie o ROS
    roscore
    
    abra o segundo terminal e inicie o turtle
    rosrun turtlesim turtlesim_node
    
    abra o terceiro terminal e inicie o KNN
    cd ros/catkin_ws
    source devel/setup.bash
    rosrun turtlesim_cleaner knnTalker.py
    
    abra o quarto terminal e inicie o listener
    cd ros/catkin_ws
    source devel/setup.bash
    rosrun turtlesim_cleaner listener.py

    
