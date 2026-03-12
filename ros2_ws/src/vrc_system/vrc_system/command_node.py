import rclpy
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

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10
        )

        self.get_logger().info('Command node started. Waiting for /voice/command...')

    def command_callback(self, msg):

        command = msg.data.lower()

        twist = Twist()

        if command == 'move forward':
            twist.linear.x = 0.5

        elif command == 'move backward':
            twist.linear.x = -0.5

        elif command == 'turn left':
            twist.angular.z = 0.5

        elif command == 'turn right':
            twist.angular.z = -0.5

        elif command == 'stop':
            twist.linear.x = 0.0
            twist.angular.z = 0.0

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

    try:
        rclpy.shutdown()
    except:
        pass


if __name__ == '__main__':
    main()
