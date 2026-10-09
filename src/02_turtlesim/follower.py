#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class follower(Node):
    def __init__(self):
        super().__init__("follower")
        self.get_info=self.create_subscription(Pose,"/turtle1/pose",self.pose_callback_turtle1,10)
        self.follower_info=self.create_subscription(Pose,"/turtle2/pose",self.pose_callback_turtle2,10)
        self.follower_output=self.create_publisher(Twist,"/turtle2/cmd_vel",10)
        self.curr_pos_1=Pose()
        self.curr_pos_2=Pose()
        self.dt=0.1 #time step for Ki
        self.angle_integral=0.0
        self.distance_integral=0.0
        self.pre_angle_error=0.0 #for Kd
        self.pre_distance_error=0.0
        self.timer=self.create_timer(0.1,self.follower_motion)
    
    def pose_callback_turtle1(self,msg:Pose):
        self.curr_pos_1=msg

    def pose_callback_turtle2(self,msg:Pose):
        self.curr_pos_2=msg
    
    def follower_motion(self):
        move=Twist()
        self.target_angle=math.atan2((self.curr_pos_1.y-self.curr_pos_2.y),(self.curr_pos_1.x-self.curr_pos_2.x)) #target to follower
        self.angle_error=self.target_angle-self.curr_pos_2.theta
        self.distance=math.sqrt(((self.curr_pos_2.x-self.curr_pos_1.x)**2)+((self.curr_pos_2.y-self.curr_pos_1.y)**2))
        self.angle_error=math.atan2(math.sin(self.angle_error),math.cos(self.angle_error))
        #Angle PID
        #Avoiding breaking down near the target zone(oscillations etc)
        if abs(self.angle_error)>0.01:
            self.angle_integral+=self.angle_error*self.dt
            self.angle_integral=max(min(self.angle_integral, 1.0),-1.0) #overshooting
            self.angle_derivative=(self.angle_error-self.pre_angle_error)/self.dt
        else:
            self.angle_integral=0.0
            self.angle_derivative=0.0
        
        move.angular.z=self.angle_error*2.0 + self.angle_integral*0.001+self.angle_derivative*0.05
        
        self.pre_angle_error=self.angle_error
        #distance PID
        if self.distance>0.01:
            self.distance_integral+=self.distance*self.dt
            self.distance_integral=max(min(self.distance_integral, 2.0),-2.0)
            self.distance_derivative=(self.distance-self.pre_distance_error)/self.dt
        else:
            self.distance_integral=0.0
            self.distance_derivative=0.0
        move.linear.x=self.distance*1.0 +self.distance_integral*0.01+self.distance_derivative*0.05
        self.pre_distance_error=self.distance

        if(abs(self.angle_error)<0.01):
            move.angular.z=0.0
        if (self.distance<0.01):
            move.linear.x=0.0
        self.follower_output.publish(move)

def main(args=None):
    rclpy.init(args=args)
    node=follower()
    rclpy.spin(node)
    rclpy.shutdown()
