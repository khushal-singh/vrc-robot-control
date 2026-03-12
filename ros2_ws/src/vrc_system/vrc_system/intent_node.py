import sys
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

sys.path.insert(0, '/mnt/d/AIS Project/vrc-robot-control')

from intent_module.intent_mapper import map_intent


class IntentNode(Node):

    def __init__(self):
        super().__init__('intent_node')

        self.subscription = self.create_subscription(
            String,
            '/asr/text',
            self.callback,
            10
        )

        self.publisher = self.create_publisher(
            String,
            '/asr/intent',
            10
        )

        self.get_logger().info('Intent node started. Waiting for /asr/text...')

    def callback(self, msg):

        result = map_intent(msg.data, 1.0)

        intent = result['intent']

        if intent == 'NO_COMMAND':
            self.get_logger().warn('Intent rejected')
            return

        output = String()
        output.data = intent.lower().replace('_', ' ')

        self.publisher.publish(output)

        self.get_logger().info(
            f'Published to /asr/intent: {output.data}'
        )


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
