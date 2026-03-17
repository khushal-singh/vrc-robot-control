import rclpy
import time

from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class VoiceMotion(Node):

    def __init__(self):
        super().__init__('voice_motion')

        self.subscription = self.create_subscription(
            String,
            '/voice/command',
            self.callback,
            10)

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        self.get_logger().info("Voice motion node started")

    def callback(self, msg):

        text = msg.data.lower()

        confirm = input(f"Recognized command: '{text}'. Execute? (y/n): ")

        if confirm.lower() != 'y':
            self.get_logger().info("Command cancelled")
            return

        cmd = Twist()

        duration = 2.0

        if "forward" in text:
            cmd.linear.x = 0.4

        elif "backward" in text:
            cmd.linear.x = -0.4

        elif "left" in text:
            cmd.angular.z = 0.8

        elif "right" in text:
            cmd.angular.z = -0.8

        elif "stop" in text:
            cmd.linear.x = 0.0
            cmd.angular.z = 0.0
            duration = 0.0

        self.publisher.publish(cmd)

        self.get_logger().info(f"Published motion for: {text}")

        # move for fixed duration
        time.sleep(duration)

        # stop automatically
        stop = Twist()
        self.publisher.publish(stop)

        self.get_logger().info("Stopped robot")


def main():
    rclpy.init()
    node = VoiceMotion()
    rclpy.spin(node)


if __name__ == '__main__':
    main()