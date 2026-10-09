#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import math

class state_machine(Node):
    def __init__(self):
        super().__init__("state_machine")
        self.sub=self.create_subscription(Pose,"/turtle1/pose",self.pose_callback_turtle1,10)
        self.pub=self.create_publisher(Twist,"/turtle1/cmd_vel",10)
        self.turtle2=self.create_subscription(Pose,"/turtle2/pose",self.pose_callback_turtle2,10)
        self.curr_pos_1=Pose()
        self.curr_pos_2=Pose()
        self.state="2"
        self.curr_state="TURN"
        self.dt=0.1 
        self.angle_integral=0.0
        self.distance_integral=0.0
        self.pre_angle_error=0.0 
        self.pre_distance_error=0.0
        self.last_turtle_spawned=self.get_clock().now()
        self.timer=self.create_timer(0.1,self.Motion)

    def pose_callback_turtle1(self,msg:Pose):
        self.curr_pos_1=msg

    def pose_callback_turtle2(self,msg:Pose):
        self.curr_pos_2=msg
        self.last_turtle_spawned=self.get_clock().now() #last time turtle sent a message

    def turn(self,curr_target):
        move=Twist()
        self.target_angle=math.atan2((4.0-self.curr_pos_1.y),(curr_target-self.curr_pos_1.x)) #target to follower
        self.angle_error=self.target_angle-self.curr_pos_1.theta
        self.angle_error=math.atan2(math.sin(self.angle_error),math.cos(self.angle_error))
        move.angular.z=self.angle_error*0.3
        move.linear.x=0.0
        if(abs(self.angle_error)<0.01):
            move.angular.z=0.0
            self.curr_state="MOVE"
        self.pub.publish(move)

    def straight(self,curr_target,next_target):
        move=Twist()
        self.distance=math.sqrt(((curr_target-self.curr_pos_1.x)**2)+((4.0-self.curr_pos_1.y)**2))
        self.target_angle=math.atan2((4.0-self.curr_pos_1.y),(curr_target-self.curr_pos_1.x)) #target to follower
        self.angle_error=self.target_angle-self.curr_pos_1.theta
        self.angle_error=math.atan2(math.sin(self.angle_error),math.cos(self.angle_error))
        move.linear.x=self.distance*1.0
        if(abs(self.angle_error)>0.01):
            move.angular.z=self.angle_error*2.0
        if(self.distance<0.1):
            move.linear.x=0.0
            self.curr_state="TURN"
            self.state=next_target
        self.pub.publish(move)

    def Motion(self):
        new_time=self.get_clock().now()
        if (new_time-self.last_turtle_spawned).nanoseconds*1e-9<0.5: #if there is a lag of more than 0.5 seconds, that means turtle despawned/not there
            move=Twist()
            self.target_angle=math.atan2((self.curr_pos_2.y-self.curr_pos_1.y),(self.curr_pos_2.x-self.curr_pos_1.x)) #target to follower
            self.angle_error=self.target_angle-self.curr_pos_1.theta
            self.distance=math.sqrt(((self.curr_pos_2.x-self.curr_pos_1.x)**2)+((self.curr_pos_2.y-self.curr_pos_1.y)**2))
            self.angle_error=math.atan2(math.sin(self.angle_error),math.cos(self.angle_error))
            #Angle PID
            if abs(self.angle_error)>0.01:
                self.angle_integral+=self.angle_error*self.dt
                self.angle_integral=max(min(self.angle_integral, 1.0),-1.0) #overshooting
                self.angle_derivative=(self.angle_error-self.pre_angle_error)/self.dt
            else:
                self.angle_integral=0.0
                self.angle_derivative=0.0
        
            move.angular.z=self.angle_error*2.0 + self.angle_integral*0.001+self.angle_derivative*0.05
            self.pre_angle_error=self.angle_error
            #Distance PID
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
            self.pub.publish(move)
        else:
            if self.state=="2":
                if(self.curr_state=="TURN"):
                    self.turn(2.0)
                elif(self.curr_state=="MOVE"):
                    self.straight(2.0,"8")

            if self.state=="8":
                if(self.curr_state=="TURN"):
                    self.turn(8.0)
                elif(self.curr_state=="MOVE"):
                    self.straight(8.0,"2")            


    
        

def main(args=None):
    rclpy.init(args=args)
    node=state_machine()
    rclpy.spin(node)
    rclpy.shutdown()
