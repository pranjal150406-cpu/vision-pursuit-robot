#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class go_to_goal_2(Node):
    def __init__(self):
        super().__init__("Go_to_goal_2")
        self.pub=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.sub=self.create_subscription(Pose,"/turtle1/pose",self.pose_callback,10)
        self.x=float(input("Enter the x coordinate: "))
        self.y=float(input("Enter the y coordinate: "))
        self.curr=Pose()
        self.dt=0.1
        self.angle_integral=0.0
        self.distance_integral=0.0
        self.pre_angle_error=0.0 
        self.pre_distance_error=0.0
        self.count=0
        self.timer=self.create_timer(0.1,self.Move_to_goal)

    def pose_callback(self,msg:Pose):
        self.curr=msg

    def Move_to_goal(self):
        move=Twist()
        self.target_angle=math.atan2((self.y-self.curr.y),(self.x-self.curr.x))
        self.angle_error=self.target_angle-self.curr.theta
        self.distance=math.sqrt(((self.x-self.curr.x)**2)+((self.y-self.curr.y)**2))
        self.angle_error=math.atan2(math.sin(self.angle_error),math.cos(self.angle_error))

        #Angle PID
        if abs(self.angle_error)>0.01:
            self.angle_integral+=self.angle_error*self.dt
            self.angle_integral=max(min(self.angle_integral, 1.0),-1.0) #overshooting
            self.angle_derivative=(self.angle_error-self.pre_angle_error)/self.dt
        else:
            self.angle_integral=0.0
            self.angle_derivative=0.0
        
        #Distance PID
        if self.distance>0.01:
            self.distance_integral+=self.distance*self.dt
            self.distance_integral=max(min(self.distance_integral, 2.0),-2.0)
            self.distance_derivative=(self.distance-self.pre_distance_error)/self.dt
        else:
            self.distance_integral=0.0
            self.distance_derivative=0.0
        move.angular.z=self.angle_error*2.0 + self.angle_integral*0.001+self.angle_derivative*0.05
        move.linear.x=self.distance*1.0 +self.distance_integral*0.01+self.distance_derivative*0.05
        self.pre_distance_error=self.distance
        self.pre_angle_error=self.angle_error
        if(self.count==0):
            print("Angle required: ",self.angle_error)
            print("Distance required: ",self.distance)
            self.count+=1

        if(abs(self.angle_error)<0.01):
            move.angular.z=0.0
        if (self.distance<0.01):
            move.linear.x=0.0
        self.pub.publish(move)


def main(args=None):
    rclpy.init(args=args)
    node=go_to_goal_2()
    rclpy.spin(node)
    rclpy.shutdown()



            

