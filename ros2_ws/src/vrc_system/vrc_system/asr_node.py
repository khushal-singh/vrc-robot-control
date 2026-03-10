import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class ASRNode(Node):

    def __init__(self):
        super().__init__('asr_node')

        self.subscription = self.create_subscription(
            String,
            '/audio/raw',
            self.audio_callback,
            10
        )

        self.publisher = self.create_publisher(
            String,
            '/asr/text',
            10
        )

        self.get_logger().info('ASR node started. Waiting for /audio/raw...')

    def audio_callback(self, msg):
        # Temporary ASR simulation
        recognized_text = String()
        recognized_text.data = 'move forward'

        self.publisher.publish(recognized_text)

        self.get_logger().info(f'Published to /asr/text: {recognized_text.data}')


def main(args=None):
    rclpy.init(args=args)

    node = ASRNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
