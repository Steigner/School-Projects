### Simple Translation Path Planning via RRT + A*

**Artificial Intelligence Algorithms Course - VAI**

```javascript
Software
```
```
OS Ubuntu 18.04
ROS Melodic
Moveit 1
```
```javascript
Programming-Language, Library
```
```
Python 2
- Python standard library
- Plotly
```

```javascript
Algorithms
```
```
A*  = v1.0
RRT = v1.0
```

This repository contain very simple approach of appliacation and comparation A* and RRT algorithm for path planning cobot UR3 from Universal Robots.

Repository contain 2 folders:

* path_planning - this ros package integrate to your catkin workaspace
* technical_report_and_presentation - folder contain technical report for this project and presentation about some ai problematics, both is in [[czech lang.]](https://en.wikipedia.org/wiki/Czech_language).

### Note
Algorithms wasn't programmed in the most elegantly way(try better heuristics, in A* for lists Open/Close use dictonary, etc ...). Main reason is attempt to avoid common solutions and get some +points.
Time of finding solution is horrible, so in conclusion for real world application is better use modification of standalone algorithms as BiRRT etc... or programmed it in C++ or some faster prog. language alternativly Julia.

### Future work

* adit for ROS Noetic -> python3
* add Greedy best first-search, BiA*, ...
* add BiRRT, GPU RRT, ...
* add option to run in C/C++ or alternativly core compute of algo in Julia with communication by **RobotOS.jl**
* create own approach of trajectory with IK, FK and smoothing trajectory by Beziér curves, etc ... (in this stage is use moveit linear trajectory)

### How to run?
#### Install dependencies
* [ROS] http://wiki.ros.org/melodic/Installation/Ubuntu
* [MOVEIT] https://moveit.ros.org/install/
* [ROS Universal Robot] https://github.com/ros-industrial/universal_robot.git
* [Universal Robots ROS Driver] https://github.com/UniversalRobots/Universal_Robots_ROS_Driver

Create catkin workspace, implicate dependent packages include **path_planning** from this repository.

#### Simulation in Gazebo
```javascript
Terminal
```
```console
user@user-pc:~$ roslaunch ur_gazebo ur3.launch
```
```console
user@user-pc:~$ roslaunch ur3_moveit_config ur3_moveit_planning_execution.launch sim:=true
```
```console
user@user-pc:~$ roslaunch ur3_moveit_config moveit_rviz.launch
```
```console
user@user-pc:~$ rosrun path_planning run.py
```
#### Real Robot
```javascript
Terminal
```
```console
user@user-pc:~$ roslaunch ur_robot_driver ur3_bringup.launch robot_ip:=xxx.xxx.xxx.xxx
```
```console
user@user-pc:~$ roslaunch ur3_moveit_config ur3_moveit_planning_execution.launch
```
```console
user@user-pc:~$ roslaunch ur3_moveit_config moveit_rviz.launch
```
```console
user@user-pc:~$ rosrun path_planning run.py
```
