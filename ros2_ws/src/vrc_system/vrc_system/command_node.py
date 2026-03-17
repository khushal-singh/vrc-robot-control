import rclpy
import time
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class CommandNode(Node):

    def __init__(self):
        super().__init__('command_node')

        self.subscription = self.create_subscription(
            String,
            '/voice/command',
            self.command_callback,
            10
        )

        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

        self.get_logger().info('Command node started.')

    def execute_motion(self, linear_x, angular_z, duration):

        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z

        start = time.time()

        while time.time() - start < duration:
            self.publisher.publish(msg)
            time.sleep(0.1)

        stop = Twist()
        self.publisher.publish(stop)

    def command_callback(self, msg):

        command = msg.data.lower()

        if command == "move forward":
            self.execute_motion(0.20, 0.0, 2.0)

        elif command == "move backward":
            self.execute_motion(-0.20, 0.0, 2.0)

        elif command == "turn left":
            self.execute_motion(0.0, 0.5, 1.5)

        elif command == "turn right":
            self.execute_motion(0.0, -0.5, 1.5)

        elif command == "stop":
            self.execute_motion(0.0, 0.0, 0.1)

        self.get_logger().info(f'Executed command: {command}')


def main(args=None):
    rclpy.init(args=args)
    node = CommandNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()