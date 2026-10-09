#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class go_to_goal(Node):
    def __init__(self):
        super().__init__("Go_to_goal")
        self.pub=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.sub=self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)
        self.x=float(input("Enter the x coordinate: "))
        self.y=float(input("Enter the y coordinate: "))
        self.poseobj=Pose()
        self.angle=math.atan2((self.y-5.544445),(self.x-5.544445)) #need to make sure of all quadrants
        self.timer=self.create_timer(0.1,self.MoveTurtle)

    def pose_callback(self,msg:Pose):
        self.poseobj=msg

    def MoveTurtle(self):
        move=Twist()
        self.angle_error=self.angle-self.poseobj.theta
        if(self.angle_error>3.14): #get it in range of -pi to pi
            self.angle_error-=2*3.14
        elif(self.angle_error<-3.14):
            self.angle_error+=2*3.14

        if(abs(self.poseobj.x-self.x)<1 and abs(self.poseobj.y-self.y)<1):  #tolerance
            move.linear.x=0.0
            move.angular.z=0.0
        else:
            if(abs(self.angle_error)>0.1): #angle tolerance
                if(self.angle_error>0):
                    move.angular.z=1.0 #move left
                else:
                    move.angular.z=-1.0 #move right
            else:
                move.linear.x=1.0
                move.angular.z=0.0
        
        self.pub.publish(move)

def main(args=None):
    rclpy.init(args=args)
    node=go_to_goal()
    rclpy.spin(node)
    rclpy.shutdown()