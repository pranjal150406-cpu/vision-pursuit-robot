#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import numpy as np
from geometry_msgs.msg import Twist

yellow=[255,0,0]

def get_limits(color):
    c=np.uint8([[color]]) #insert bgr values which will get converted to hsv valurd
    hsvC=cv2.cvtColor(c,cv2.COLOR_BGR2HSV)

    lowerLimit= hsvC[0][0][0]-10,100,100
    upperLimit= hsvC[0][0][0]+10,255,255

    lowerLimit=np.array(lowerLimit,dtype=np.uint8)
    upperLimit=np.array(upperLimit,dtype=np.uint8)

    return lowerLimit,upperLimit

class color_detector(Node):
    def __init__(self):
        super().__init__("Color_Detector")
        self.bridge=CvBridge()
        self.object_present=False
        self.curr_x=0.0
        self.curr_y=0.0
        self.sub=self.create_subscription(Image,'/camera/image_raw',self.image_callback,10)
        self.pub=self.create_publisher(Twist,"/cmd_vel",10)



    def image_callback(self,msg):
        move=Twist()
        self.object_present=False
        frame=self.bridge.imgmsg_to_cv2(msg,desired_encoding="bgr8")
        hsvImage=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV) #converting image from bgr to hsv

        lowerLimit,upperLimit=get_limits(color=yellow)
    
        mask=cv2.inRange(hsvImage,lowerLimit,upperLimit) #binary mask which detects the color as white

        contours,heirarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #finding contours

        frame=cv2.drawContours(frame,contours,-1,(0,0,255),5) 
        for contour in contours:
            area=cv2.contourArea(contour)

            if area>500: #ignore small areas
                self.object_present=True
                moments=cv2.moments(contour)
                if moments["m00"]!=0: #avoiding div by 0
                    cx=int(moments["m10"]/moments["m00"])
                    cy=int(moments["m01"]/moments["m00"])
                    #centroid coordinates
                    cv2.circle(frame,(cx,cy),2,(0,0,255),-1)

                    #finding whether target object is left or right
                    self.image_center=frame.shape[1]//2
                    self.angle_error=cx-self.image_center
                    move.angular.z=-self.angle_error*0.001
                    move.linear.x=0.15
                    if(abs(self.angle_error)<20):
                        move.angular.z=0.0

                    if area>200000:
                        move.linear.x=0.0
                        move.angular.z=0.0
 
        
        if self.object_present==False:
            move.angular.z=0.3
            move.linear.x=0.0

        self.pub.publish(move)



        cv2.imshow('frame',frame)
        cv2.waitKey(1) #wait a millisecond for key press


def main(args=None):
    rclpy.init(args=args)
    node=color_detector()
    rclpy.spin(node)
    node.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__=="__main__":
    main()

