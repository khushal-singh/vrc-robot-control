import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class AudioInputNode(Node):

    def __init__(self):
        super().__init__('audio_input_node')

        self.publisher = self.create_publisher(
            String,
            '/audio/raw',
            10
        )

        self.has_published = False

        self.timer = self.create_timer(2.0, self.publish_audio)

        self.get_logger().info('Audio input node started.')

    def publish_audio(self):
        if self.has_published:
            return

        msg = String()
        msg.data = 'audio_dataset/clean/sample.wav'

        self.publisher.publish(msg)

        self.get_logger().info(f'Publishing: {msg.data}')

        self.has_published = True


def main(args=None):
    rclpy.init(args=args)

    node = AudioInputNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
