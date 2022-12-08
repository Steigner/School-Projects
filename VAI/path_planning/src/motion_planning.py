#!/usr/bin/env python

# main system and ROS library
import sys
import rospy

# library for get info from robot and also control robot
import moveit_commander
import geometry_msgs.msg

import copy
from math import pi
from moveit_commander.conversions import pose_to_list


def all_close(goal, actual, tolerance):
  all_equal = True
  if type(goal) is list:
    for index in range(len(goal)):
      if abs(actual[index] - goal[index]) > tolerance:
        return False

  elif type(goal) is geometry_msgs.msg.PoseStamped:
    return all_close(goal.pose, actual.pose, tolerance)

  elif type(goal) is geometry_msgs.msg.Pose:
    return all_close(pose_to_list(goal), pose_to_list(actual), tolerance)

  return True

class Robot_Control(object):
    def __init__(self):
        moveit_commander.roscpp_initialize(sys.argv)
        rospy.init_node('TESTOS', anonymous=True)
        robot = moveit_commander.RobotCommander()
        scene = moveit_commander.PlanningSceneInterface()
        move_group = moveit_commander.MoveGroupCommander("manipulator")

        self.box_name = ''
        self.scene = scene
        self.robot = robot
        self.move_group = move_group

    # in this method is defined intit position, if we call this method
    # robot get to this position
    def init_motion(self):
        move_group = self.move_group

        # set up for velocity, accerelation
        move_group.set_max_velocity_scaling_factor(0.5)
        move_group.set_max_acceleration_scaling_factor(0.5)

        # some allow_replanning, and other stuff.
        move_group.allow_replanning(True)
        move_group.allow_looking(True)

        # set up in joints goal, which is defined in radians
        joint_goal = move_group.get_current_joint_values()
        joint_goal[0] = 0
        joint_goal[1] = -pi/2
        joint_goal[2] = 0
        joint_goal[3] = -pi/2
        joint_goal[4] = -pi/2
        joint_goal[5] = pi/2

        # go to defined joint goal
        move_group.go(joint_goal, wait=True)
        move_group.stop()

        current_joints = move_group.get_current_joint_values()
        return all_close(joint_goal, current_joints, 0.01)

    # method which is called from run.py, and this method is used for
    # go by all finded points by defined algorithms
    def plan_cartesian_path(self, x,y,z):
        group = self.move_group

        waypoints = []
        wpose = group.get_current_pose().pose

        for i in range(len(x)-3,-1,-1):
          wpose.position.x = round(x[i],2)
          wpose.position.y = round(y[i],2)
          wpose.position.z = round(z[i],2)
          waypoints.append(copy.deepcopy(wpose))

        (plan, fraction) = group.compute_cartesian_path(waypoints, 0.05, 0.0, avoid_collisions = True, path_constraints = None)

        # go by cumputed path
        group.execute(plan, wait=True)

  #--------------------------------PLANNING SCENE----------------------------------------------
    def add_box(self,timeout=4):
        box_name = self.box_name
        scene = self.scene
        box_pose = geometry_msgs.msg.PoseStamped()
        box_pose.header.frame_id = "world"

        box_pose.pose.position.x = 0
        box_pose.pose.position.y = 0
        box_pose.pose.position.z = -0.05
        box_name = "plane"
        scene.add_box(box_name, box_pose, size=(2, 2, 0.1))

        self.box_name=box_name
        return self.wait_for_state_update(box_is_known=True, timeout=timeout)

    def end_box(self,timeout=4):
        box_name = self.box_name
        scene = self.scene
        box_pose = geometry_msgs.msg.PoseStamped()
        box_pose.header.frame_id = "world"

        box_pose.pose.position.x = 0.37
        box_pose.pose.position.y = 0.11
        box_pose.pose.position.z = 0.55
        box_name = "end_box"
        scene.add_box(box_name, box_pose, size=(0.05, 0.05, 0.05))

        self.box_name=box_name
        return self.wait_for_state_update(box_is_known=True, timeout=timeout)

    def wait_for_state_update(self, box_is_known=False, box_is_attached=False, timeout=4):
        box_name = self.box_name
        scene = self.scene
        start = rospy.get_time()
        seconds = rospy.get_time()
        while (seconds - start < timeout) and not rospy.is_shutdown():
            attached_objects = scene.get_attached_objects([box_name])
            is_attached = len(attached_objects.keys()) > 0
            is_known = box_name in scene.get_known_object_names()
            if (box_is_attached == is_attached) and (box_is_known == is_known):
                return True
        rospy.sleep(0.1)
        seconds = rospy.get_time()
        return False

    def remove_box(self):
        scene = self.scene
        scene.remove_world_object()
