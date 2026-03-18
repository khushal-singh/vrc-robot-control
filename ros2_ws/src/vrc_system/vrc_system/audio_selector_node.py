import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import os

BASE_PATH = "/mnt/d/AIS Project/vrc-robot-control/audio_dataset/clean"


class AudioSelectorNode(Node):

    def __init__(self):
        super().__init__('audio_selector_node')

        self.publisher_ = self.create_publisher(
            String,
            '/audio/filepath',
            10)

        self.run_selector()

    def run_selector(self):

        while rclpy.ok():

            speakers = sorted([
                d for d in os.listdir(BASE_PATH)
                if os.path.isdir(os.path.join(BASE_PATH, d))
            ])

            print("\nAvailable Speakers:")
            for i, spk in enumerate(speakers):
                print(f"{i+1}. {spk}")

            speaker_choice = int(input("\nSelect speaker number: ")) - 1
            speaker = speakers[speaker_choice]

            speaker_path = os.path.join(BASE_PATH, speaker)

            files = sorted([
                f for f in os.listdir(speaker_path)
                if f.endswith(".wav")
            ])

            print("\nAvailable Commands:")
            for i, f in enumerate(files):
                print(f"{i+1}. {f}")

            file_choice = int(input("\nSelect command number: ")) - 1
            selected_file = files[file_choice]

            full_path = os.path.join(speaker_path, selected_file)

            msg = String()
            msg.data = full_path

            # publish only once
            self.publisher_.publish(msg)

            self.get_logger().info(f"Published: {full_path}")


def main():
    rclpy.init()
    node = AudioSelectorNode()
    rclpy.spin(node)


if __name__ == '__main__':
    main()