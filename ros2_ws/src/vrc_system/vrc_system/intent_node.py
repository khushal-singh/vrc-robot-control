import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class IntentNode(Node):

    def __init__(self):
        super().__init__('intent_node')

        self.subscription = self.create_subscription(
            String,
            '/asr/text',
            self.text_callback,
            10
        )

        self.publisher = self.create_publisher(
            String,
            '/asr/intent',
            10
        )

        self.get_logger().info('Intent node started. Waiting for /asr/text...')

    def text_callback(self, msg):
        intent = String()
        intent.data = msg.data.strip().lower()

        self.publisher.publish(intent)

        self.get_logger().info(f'Published to /asr/intent: {intent.data}')


def main(args=None):
    rclpy.init(args=args)

    node = IntentNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
