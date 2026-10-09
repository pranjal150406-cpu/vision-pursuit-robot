#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class DrawPolygonNode(Node):
    def __init__(self):
        super().__init__("Draw_Polygon")
        self.num_of_sides=int(input("Enter the number of sides: "))
        self.pub=self.create_publisher(Twist, "/turtle1/cmd_vel",10)
        self.count=0
        self.angle=(2*3.14)/self.num_of_sides #exterior angle
        self.timer=self.create_timer(1,self.DrawPolygon)

    def DrawPolygon(self):
        msg=Twist()
        if self.count%2==0:
            msg.linear.x=1.0
        else:
            msg.angular.z=self.angle
        
        self.pub.publish(msg)
        self.count+=1
        if(self.count>(2*self.num_of_sides)-1):
            msg.linear.x=0.0
            msg.angular.z=0.0
            self.pub.publish(msg)
            self.destroy_timer(self.timer)

def main(args=None):
    rclpy.init(args=args)
    node=DrawPolygonNode()
    rclpy.spin(node)
    rclpy.shutdown()

