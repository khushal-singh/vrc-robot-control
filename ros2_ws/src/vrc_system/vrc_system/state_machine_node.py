
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class StateMachineNode(Node):

    def __init__(self):
        super().__init__('state_machine_node')

        self.subscription = self.create_subscription(
            String,
            '/asr/intent',
            self.intent_callback,
            10
        )

        self.publisher = self.create_publisher(
            String,
            '/voice/command',
            10
        )

        self.pending_command = None
        self.state = 'IDLE'

        self.timer = None

        self.get_logger().info('State machine node started.')

    def intent_callback(self, msg):
        command = msg.data.strip().lower()

        # Emergency stop executes immediately
        if command == 'stop':
            self.publish_command(command)
            return

        # Waiting for confirmation
        if self.state == 'IDLE':
            if command in ['move forward', 'move backward', 'turn left', 'turn right']:
                self.pending_command = command
                self.state = 'WAITING_CONFIRMATION'

                self.get_logger().info(
                    f'Pending command: {command}. Waiting for yes/no...'
                )

                self.start_timeout()

        elif self.state == 'WAITING_CONFIRMATION':
            if command == 'yes':
                self.publish_command(self.pending_command)

                self.pending_command = None
                self.state = 'IDLE'

                self.cancel_timeout()

            elif command == 'no':
                self.get_logger().info('Command cancelled.')

                self.pending_command = None
                self.state = 'IDLE'

                self.cancel_timeout()

    def publish_command(self, command):
        output = String()
        output.data = command

        self.publisher.publish(output)

        self.get_logger().info(f'Published to /voice/command: {command}')

    def start_timeout(self):
        self.cancel_timeout()
        self.timer = self.create_timer(5.0, self.timeout_callback)

    def cancel_timeout(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None

    def timeout_callback(self):
        self.get_logger().info('Timeout reached. Command discarded.')

        self.pending_command = None
        self.state = 'IDLE'

        self.cancel_timeout()


def main(args=None):
    rclpy.init(args=args)

    node = StateMachineNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
