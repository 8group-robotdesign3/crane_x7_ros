#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import geometry_msgs.msg
import rosnode
from tf.transformations import quaternion_from_euler
from trajectory_msgs.msg import JointTrajectoryPoint
from control_msgs.msg import ( GripperCommandAction, GripperCommandGoal )
import time


def main():
    rospy.init_node("crane_x7_pick_and_place_controller")
    robot = moveit_commander.RobotCommander()
    arm = moveit_commander.MoveGroupCommander("arm")
    arm.set_max_velocity_scaling_factor(0.1)
    gripper = moveit_commander.MoveGroupCommander("gripper")

    while len([s for s in rosnode.get_node_names() if 'rviz' in s]) == 0:
        rospy.sleep(1.0)
    rospy.sleep(1.0)

    print("Group names:")
    print(robot.get_group_names())

    print("Current state:")
    print(robot.get_current_state())

    # アーム初期ポーズを表示
    arm_initial_pose = arm.get_current_pose().pose
    print("Arm initial pose:")
    print(arm_initial_pose)

    # 何かを掴んでいた時のためにハンドを開く
    gripper.set_joint_value_target([0.9, 0.9])
    gripper.go()

    # SRDFに定義されている"home"の姿勢にする
    arm.set_named_target("home")
    arm.go()
    gripper.set_joint_value_target([0.7, 0.7])
    gripper.go()
    
   
    # 掴む準備をする
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = 0.2
    target_pose.position.y = 0.0
    target_pose.position.z = 0.2
    q = quaternion_from_euler(-3.14, 0.0, -3.14/2.0)  # 上方から掴みに行く場合
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]
    arm.set_pose_target(target_pose)  # 目標ポーズ設定
    arm.go()  # 実行

    # ハンドを開く
    gripper.set_joint_value_target([0.7, 0.7])
    gripper.go()

    # 掴みに行く
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = 0.2
    target_pose.position.y = 0.0
    target_pose.position.z = 0.0875
    q = quaternion_from_euler(-3.14, 0.0, -3.14/2.0)  # 上方から掴みに行く場合
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]
    arm.set_pose_target(target_pose)  # 目標ポーズ設定
    arm.go()  # 実行

    # ハンドを閉じる
    gripper.set_joint_value_target([0.13, 0.13])
    gripper.go()

    # 持ち上げる
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = 0.2
    target_pose.position.y = 0.0
    target_pose.position.z = 0.3
    q = quaternion_from_euler(-3.14, 0.0, -3.14/2.0)  # 上方から掴みに行く場合
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]
    arm.set_pose_target(target_pose)  # 目標ポーズ設定
    arm.go()							# 実行

    #投げ始める位置まで移動
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = 0.35
    target_pose.position.y = 0.0
    target_pose.position.z = 0.3
    q = quaternion_from_euler(-3.14, 0.0, -3.14/2.0)  # 上方から掴みに行く場合
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]
    arm.set_pose_target(target_pose)  # 目標ポーズ設定
    arm.go()							# 実行

    arm.set_max_velocity_scaling_factor(0.8)
  
    #投げ途中
   # target_pose = geometry_msgs.msg.Pose()
   # target_pose.position.x = -0.2
   # target_pose.position.y = 0.3
   # target_pose.position.z = 0.25
   # q = quaternion_from_euler(-3.14*4.0/3.0, 0.0, -3.14/2.0)  # 上方から掴みに行く場合
   # target_pose.orientation.x = q[0]
   # target_pose.orientation.y = q[1]
   # target_pose.orientation.z = q[2]
   # target_pose.orientation.w = q[3]
   # arm.set_pose_target(target_pose)  # 目標ポーズ設定
   # arm.go()# 実行

    arm.set_max_velocity_scaling_factor(1.0)
   # gripper.set_joint_value_target([1.0, 1.0])

    # 投げ終わり
    target_pose = geometry_msgs.msg.Pose()
    target_pose.position.x = -0.15
    target_pose.position.y = -0.15
    target_pose.position.z = 0.5
    q = quaternion_from_euler(3.14/3.0, 0.0, -3.14/2.0)
    target_pose.orientation.x = q[0]
    target_pose.orientation.y = q[1]
    target_pose.orientation.z = q[2]
    target_pose.orientation.w = q[3]
    arm.set_pose_target(target_pose)
    arm.go()
 
   # rospy.sleep(0.05)
    # ハンドを開く
    gripper.set_joint_value_target([1.0, 1.0])
    gripper.go()
   
    
    rospy.sleep(0.5)

    #ハンドを閉じる
    gripper.set_joint_value_target([0.2, 0.2])
    gripper.go()

    arm.set_max_velocity_scaling_factor(0.1)


    # SRDFに定義されている"home"の姿勢にする
    arm.set_named_target("home")
    arm.go()

    print("done")


if __name__ == '__main__':

    try:
        if not rospy.is_shutdown():
            main()
    except rospy.ROSInterruptException:
        pass
