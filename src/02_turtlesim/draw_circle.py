#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DrawCircle2(Node):
    def __init__(self):
        super().__init__("Draw_Circle_2")
        self.pub=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.count=0
        self.timer=self.create_timer(3.0,self.Drawing)
        #radius is not based on linear velocity, it is a ratio of linear and angular properties

    def Drawing(self):
        msg=Twist()
        if(self.count==0):
            msg.linear.x=7.0 #this means it covers 7 units not the radius is 7 units
            msg.angular.z=2*3.14
            self.count+=1
            self.pub.publish(msg)

        else:
            msg.linear.x=0.0
            msg.angular.z=0.0
            self.pub.publish(msg)
            self.destroy_timer(self.timer)


def main(args=None):
    rclpy.init(args=args)
    node=DrawCircle2()
    rclpy.spin(node)
    rclpy.shutdown()