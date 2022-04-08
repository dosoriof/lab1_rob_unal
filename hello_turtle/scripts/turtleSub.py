#!/usr/bin/env python
import rospy
from turtlesim.msg import Pose
import time

def callback(data):
    rospy.loginfo(data.x)
    rospy.loginfo(data.y)
    # rospy.loginfo(data.theta)
    # rospy.loginfo(data.linear_velocity)
    # rospy.loginfo(data.angular_velocity)
    print(rospy.Time.now())

    
def pose():
    rospy.init_node('poseSub', anonymous=True)
    rospy.Subscriber("turtle1/pose", Pose, callback)
    rospy.spin()

if __name__ == '__main__':
    pose()