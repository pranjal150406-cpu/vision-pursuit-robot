#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class Boundry(Node):
    def __init__(self):
        super().__init__("Boundry")
        self.sub=self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)
        self.pub=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.poseobj=Pose()
        self.timer=self.create_timer(0.1,self.MoveTurtle) #callback needs to be faster

    def pose_callback(self,msg:Pose):
        self.poseobj=msg
    
    def MoveTurtle(self):
        move=Twist()
        if(self.poseobj.x>9.5 or self.poseobj.x<1.5 or self.poseobj.y>9.5 or self.poseobj.y<1.5): #turtlesim window is 11*11
            move.linear.x=1.0
            move.angular.z=3.14/4
        
        else:
            move.linear.x=1.0
            move.angular.z=0.0

        self.pub.publish(move)
    



def main(args=None):
    rclpy.init(args=args)
    node=Boundry()
    rclpy.spin(node)
    rclpy.shutdown()