import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import os


class AudioInputNode(Node):

    def __init__(self):
        super().__init__('audio_input_node')

        self.publisher = self.create_publisher(
            String,
            '/audio/raw',
            10
        )

        self.timer = self.create_timer(
            5.0,
            self.publish_audio
        )

        self.base_path = "/mnt/d/AIS Project/vrc-robot-control/audio_dataset/clean"

        self.audio_files = []
        self.current_index = 0

        self.load_audio_files()

        self.get_logger().info('Audio input node started.')

    def load_audio_files(self):

        command_order = [
            "MoveForward.wav",
            "MoveBackward.wav",
            "TurnLeft.wav",
            "TurnRight.wav",
            "Stop.wav"
        ]

        for speaker in sorted(os.listdir(self.base_path)):

            speaker_path = os.path.join(self.base_path, speaker)

            if os.path.isdir(speaker_path):

                for command in command_order:

                    file_path = os.path.join(speaker_path, command)

                    if os.path.exists(file_path):
                        self.audio_files.append(file_path)

    def publish_audio(self):

        if self.current_index >= len(self.audio_files):
            self.get_logger().info('All audio files processed.')
            self.timer.cancel()
            return

        full_path = self.audio_files[self.current_index]

        msg = String()
        msg.data = full_path

        self.publisher.publish(msg)

        self.get_logger().info(f'Publishing: {full_path}')

        self.current_index += 1


def main(args=None):

    rclpy.init(args=args)

    node = AudioInputNode()

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
