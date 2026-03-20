import sys
import os
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# Make project root importable
sys.path.insert(0, '/mnt/d/AIS Project/vrc-robot-control')


class ASRNode(Node):

    def __init__(self):
        super().__init__('asr_node')

        # Subscribe to file paths selected by AudioSelectorNode
        self.subscription = self.create_subscription(
            String,
            '/audio/filepath',
            self.audio_callback,
            10
        )

        # Publish recognized text commands for VoiceMotion
        self.publisher = self.create_publisher(
            String,
            '/voice/command',
            10
        )

        # Lazy handle to transcribe() so startup is fast
        self._transcribe_fn = None

        self.get_logger().info('ASR node started. Waiting for /audio/filepath...')

    # Load ASR engine only once, on first command
    def _lazy_load_transcriber(self):
        if self._transcribe_fn is None:
            self.get_logger().info('Loading ASR engine (transcribe)...')
            from asr_module.asr_engine import transcribe
            self._transcribe_fn = transcribe
            self.get_logger().info('ASR engine loaded.')

    def audio_callback(self, msg: String):
        wav_path = msg.data.strip()
        self.get_logger().info(f"Received path: {wav_path}")

        if not os.path.isfile(wav_path):
            self.get_logger().error(f'File not found: {wav_path}')
            return

        # Ensure ASR engine is loaded
        self._lazy_load_transcriber()

        # Protect against ASR crashes
        try:
            result = self._transcribe_fn(wav_path)
        except Exception as e:
            self.get_logger().error(f"ASR transcribe() failed: {e}")
            return

        self.get_logger().info(f"ASR result: {result}")

        confidence = result.get('confidence', 0.0)
        text = result.get('text', '').strip()

        if confidence >= 0.30 and text:
            output = String()
            output.data = text
            self.publisher.publish(output)
            self.get_logger().info(
                f"Published to /voice/command: '{text}' (conf={confidence:.2f})"
            )
        else:
            self.get_logger().warn(
                f"Rejected low confidence: conf={confidence:.2f}"
            )


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
