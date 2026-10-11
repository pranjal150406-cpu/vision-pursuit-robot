#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data #changing it from reliability to best effort

class obstacle_detector(Node):
    def __init__(self):
        super().__init__("obstacle_detector")
        self.sub=self.create_subscription(LaserScan,"/scan",self.scan_callback,qos_profile_sensor_data)
        self.pub=self.create_publisher(Twist,"/cmd_vel",10)
        self.lidar=None #initliase
        self.state="FORWARD"
        self.direction="LEFT"
        self.timer=self.create_timer(0.1,self.avoider)


    def scan_callback(self,msg):
        self.lidar=msg

    def avoider(self):
        if self.lidar is None: #wait for data to arrive otherwise null lists,null everything
            return
        move=Twist()
        self.len=len(self.lidar.ranges)
        self.center=self.len//2
        #dont worry about wrap around,lidar usually have thousands of readings
        self.left=self.lidar.ranges[0:self.center-30]
        self.forward=self.lidar.ranges[self.center-30:self.center+30]
        self.right=self.lidar.ranges[self.center+30:]
        self.left_obstacle=min(self.left)
        self.forward_obstacle=min(self.forward)
        self.right_obstacle=min(self.right)
        if self.state=="FORWARD": #break into states to prevent oscillation
            if self.forward_obstacle<0.75:
                self.state="TURN"
                if self.right_obstacle<self.left_obstacle:
                    self.direction="LEFT"
                else:
                    self.direction="RIGHT"

            else:
                move.angular.z=0.0
                move.linear.x=0.3

        elif self.state=="TURN":
            move.linear.x=0.0
            if self.direction=="LEFT":
                move.angular.z=1.0
            else:
                move.angular.z=-1.0

            if self.forward_obstacle>0.75:  #to go back to forward direction
                self.state="FORWARD"
        self.pub.publish(move)



        



def main(args=None):
    rclpy.init(args=args)
    node=obstacle_detector()
    rclpy.spin(node)
    rclpy.shutdown()

