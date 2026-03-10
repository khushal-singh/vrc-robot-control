import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class CommandNode(Node):

    def __init__(self):
        super().__init__('command_node')

        # Subscribe to /voice/command
        self.subscription = self.create_subscription(
            String,
            '/voice/command',
            self.command_callback,
            10
        )

        # Publish robot velocity commands to /cmd_vel
        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.get_logger().info('Command node started. Waiting for /voice/command...')

    def command_callback(self, msg):
        command = msg.data.strip().lower()

        twist = Twist()

        # Fixed command vocabulary from project plan
        if command == 'move forward':
            twist.linear.x = 0.5
            twist.angular.z = 0.0

        elif command == 'move backward':
            twist.linear.x = -0.5
            twist.angular.z = 0.0

        elif command == 'turn left':
            twist.linear.x = 0.0
            twist.angular.z = 0.5

        elif command == 'turn right':
            twist.linear.x = 0.0
            twist.angular.z = -0.5

        elif command == 'stop':
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        else:
            self.get_logger().warning(f'Unknown command received: {command}')
            return

        # Publish Twist message
        self.publisher.publish(twist)

        self.get_logger().info(
            f'Published /cmd_vel → linear.x={twist.linear.x}, angular.z={twist.angular.z}'
        )


def main(args=None):
    rclpy.init(args=args)

    node = CommandNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
