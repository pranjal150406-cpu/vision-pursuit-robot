#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DrawSquareNode(Node):
    def __init__(self):
        super().__init__("Draw_Square")
        self.pub=self.create_publisher(Twist, "/turtle1/cmd_vel",10)
        self.count=0
        self.timer=self.create_timer(3,self.DrawSquare)

    def DrawSquare(self):
        msg=Twist()
        if self.count%2==0:
            msg.linear.x=2.0
            msg.angular.z=0.0
        else:
            msg.angular.z=1.57
            msg.linear.x=0.0

        self.count+=1
        self.pub.publish(msg)

        if self.count>7:
            msg.linear.x=0.0 
            msg.angular.z=0.0
            self.pub.publish(msg)
            self.destroy_timer(self.timer)
        

def main(args=None):
    rclpy.init(args=args)
    node=DrawSquareNode()
    rclpy.spin(node)
    rclpy.shutdown()

