#! /usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
import moveit_commander
import geometry_msgs.msg
from std_msgs.msg import Int32
import rosnode
from tf.transformations import quaternion_from_euler

robot = moveit_commander.RobotCommander()
arm = moveit_commander.MoveGroupCommander("arm")

finish = True

def call(data):
    #rospy.loginfo('call callback function')
    global finish
    if data.data == 0 and finish:
        global robot
        global arm
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
        gripper.set_joint_value_target([0.14, 0.14])
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
        arm.go()    

        # 下ろす
        target_pose = geometry_msgs.msg.Pose()
        target_pose.position.x = 0.35
        target_pose.position.y = 0.0
        target_pose.position.z = 0.31
        q = quaternion_from_euler(-3.14, 0.0, -3.14/2.0)  # 上方から掴みに行く場合
        target_pose.orientation.x = q[0]
        target_pose.orientation.y = q[1]
        target_pose.orientation.z = q[2]
        target_pose.orientation.w = q[3]
        arm.set_pose_target(target_pose)  # 目標ポーズ設定
        arm.go()  # 実行
        
        pub = rospy.Publisher("main_node/report_progress",Int32,queue_size = 1)
        rospy.loginfo("finish")
        finish = False
        progress = 1
        for i in range(100):
            pub.publish(progress)
            rospy.loginfo("publish progress1")
        #rospy.signal_shutdown("shutdown node1")
        rospy.loginfo("finish pickup")
    #else:
    #   if finish:
    #        rospy.loginfo("not receive start sign")
def main_func():
    sub = rospy.Subscriber("main_node/activate_node",Int32,call)
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node("node1_pickup",anonymous=True)
    rospy.loginfo("success init node1")
    try:
        if not rospy.is_shutdown():
            main_func()
    except rospy.ROSInterruptException:
        pass
