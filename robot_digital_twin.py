import math
import threading
import time
from math import cos, pi, sin

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from std_msgs.msg import String


class RobotDigitalTwin(Node):

    x = 0.0
    y = 0.0
    z = 0.5
    angle = 0.0 
    th = 0.0
        

    def listener_callback(self, msg):
        command = msg.data[0:5] 
        value = int(msg.data[6:11]) 
        print(command)
        print(value)

        if(command == "MOVEFW"):
            if(value == 1000): 
                print("robot moving forward")
                vx = 0.1
                delta_x = vx * cos(self.th)
                delta_y = vx * sin(self.th)
                delta_th = 0 
                self.x += delta_x
                self.y += delta_y
                self.th += delta_th


        elif(command == "MOVEBW"):
            if(value == 1000): 
                print("robot moving backwards")
                vx = 0.1 
                delta_x = vx * cos(self.th)
                delta_y = vx * sin(self.th)
                delta_th = 0 
                self.x -= delta_x
                self.y -= delta_y
                self.th -= delta_th

        elif(command == "TURNR"):
            print("robot turning RIGHT")
            if(value == 100):
                self.angle = (self.angle - 10)
                if (self.angle < 0): self.angle = 360 - abs(self.angle)
                self.th = math.radians(self.angle)
                

        elif(command == "TURNL"):
            print("robot turning LEFT")
            if(value == 100):
                self.angle = ((10 + self.angle) % 360 ) 
                self.th = math.radians(self.angle) 
        

        elif(command == "CMOVEFW"):
            if(value == 2000): 
                print("continue robot moving forward")
                vx = 0.1 
                delta_x = vx * cos(self.th)
                delta_y = vx * sin(self.th)
                delta_th = 0 
                self.x += delta_x
                self.y += delta_y
                self.th += delta_th


        elif(command == "CMOVEBW"):
            if(value == 2000): 
                print("continue robot moving backwards")
                vx = 0.1
                delta_x = vx * cos(self.th)
                delta_y = vx * sin(self.th)
                delta_th = 0 
                self.x -= delta_x
                self.y -= delta_y
                self.th -= delta_th

        print(self.x)        
        print(self.y)
        print(self.z)
        print(self.angle)
        print(self.th)
    
    def __init__(self):
        super().__init__('robot_digital_twin')

        self.subscription = self.create_subscription(
            String,
            '/robot/control',
            self.listener_callback,
            10)
        self.subscription 

        self.publish_thread = threading.Thread(target=self._publish_thread)
        self.publish_thread.daemon = True
        self.publish_thread.start()
        
            
    def _publish_thread(self):
        while(True):
            self.publisher = self.create_publisher(Twist, '/robot/pose', 10)
            msg = Twist()
            msg.linear.x = self.x
            msg.linear.y = self.y
            msg.linear.z = self.z
            msg.angular.x = 0.0
            msg.angular.y = 0.0
            msg.angular.z = self.th

            self.publisher.publish(msg)
            self.get_logger().info("Publishing to /robot/pose")
            time.sleep(0.2)


def main(args=None):
    rclpy.init(args=args)

    robot = RobotDigitalTwin()
    rclpy.spin(robot)
    
    robot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
