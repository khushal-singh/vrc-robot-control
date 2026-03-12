import sys
import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

sys.path.insert(0, '/mnt/d/AIS Project/vrc-robot-control')

from asr_module.asr_engine import transcribe


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
        wav_path = msg.data.strip()

        self.get_logger().info(f"Received path: {repr(wav_path)}")

        if not os.path.isfile(wav_path):
            self.get_logger().error(f'File not found: {wav_path}')
            return

        result = transcribe(wav_path)

        self.get_logger().info(f"ASR result: {result}")

        if result['confidence'] >= 0.40:
            output = String()
            output.data = result['text']

            self.publisher.publish(output)

            self.get_logger().info(
                f"Published to /asr/text: {result['text']}"
            )
        else:
            self.get_logger().warn(
                f"Low confidence ignored: {result['confidence']}"
            )


def main(args=None):
    rclpy.init(args=args)

    node = ASRNode()

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
