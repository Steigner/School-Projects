#!/usr/bin/env python

# import script for compute motion planning robotic arm
from motion_planning import Robot_Control

# import main functions of scripts with algorithms
from rrt import rrt
from a_star import a_star

# main library for possibility to use ROS
import rospy

#           SPACE
S_POINT = [0.13, 0.11, 0.55]
E_POINT = [0.35, 0.11, 0.55]
GRAPH   = [0.1, 0.36, 0, 0.15, 0.5, 0.6]

#            A*
SUB = 100   # subdivision

#           RRT
N = 500     # number of iterations
A = 30      # attempts

def main():
    try:
        # first is inicialized robot with ROS, and Moveit framework
        robot = Robot_Control()

        # add box as floor, for case if robot go by bad cfg
        rospy.sleep(2)
        robot.add_box()

        # add box, for visualize end point
        robot.end_box()

        # inicialization motion to init position
        robot.init_motion()

        print("----------------------")
        print("--------MENU----------")
        print("[INFO] Which algorithm you'll want to test it?")
        print("[INFO] [1] - A*")
        print("[INFO] [2] - RRT")

        # simple UI switch, 1 == a star, 2 == rrt, 3 == exception
        try:
            x = int(input('Enter your choose: '))

        except ValueError:
            return "[INFO] That was no valid option!"

        if x == 1:
            x, y, z = a_star(S_POINT, E_POINT, GRAPH, SUB)

        elif x == 2:
            x, y, z = rrt(S_POINT,E_POINT,GRAPH,A,N)

        else:
            print("[INFO] You put wrong option!")

        robot.plan_cartesian_path(x,y,z)

        robot.remove_box()

    except rospy.ROSInterruptException:
        return
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
