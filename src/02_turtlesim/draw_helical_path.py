#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DrawHelixNode(Node):
    def __init__(self):
        super().__init__("Draw_a_helical_path")
        self.pub=self.create_publisher(Twist, "/turtle1/cmd_vel",10)
        self.motion="RCIRCLE"
        self.count=0
        self.timer=self.create_timer(1,self.DrawHelix)

    def DrawHelix(self):
        msg=Twist()
        msg.angular.z=3.14
        if self.motion=='RCIRCLE':
            msg.linear.x=2.0
            self.motion="LCIRCLE"

        else:
            msg.linear.x=1.0
            self.motion="RCIRCLE"

        self.count+=1
        self.pub.publish(msg)
        if(self.count>8):
            self.destroy_timer(self.timer)


def main(args=None):
    rclpy.init(args=args)
    node=DrawHelixNode()
    rclpy.spin(node)
    rclpy.shutdown()
