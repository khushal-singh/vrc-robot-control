import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class VoiceMotion(Node):

    def __init__(self):
        super().__init__('voice_motion')

        self.subscription = self.create_subscription(
            String,
            '/voice/command',
            self.callback,
            10)

        self.publisher = self.create_publisher(
            Twist,
            '/cmd_vel',
            10)

        self.stop_timer = None

        self.get_logger().info("Voice motion node started")

    def callback(self, msg):

        text = msg.data.lower().strip()

        confirm = input(f"Recognized command: '{text}'. Execute? (y/n): ")

        if confirm.lower() != 'y':
            self.get_logger().info("Command cancelled")
            return

        cmd = Twist()
        duration = 2.0

        if any(word in text for word in ["forward", "move forward", "go forward"]):
           cmd.linear.x = 0.4

        elif any(word in text for word in [
            "backward",
            "back",
            "move backward",
            "the back went",
            "back went"
        ]):
            cmd.linear.x = -0.4

        elif any(word in text for word in [
            "left",
            "turn left",
            "on left"
        ]):
            cmd.angular.z = 0.8

        elif any(word in text for word in [
            "right",
            "turn right"
        ]):
            cmd.angular.z = -0.8

        elif "stop" in text:
            duration = 0.0

        else:
            self.get_logger().info(f"Unknown command: {text}")
            return        
        # publish motion immediately
        self.publisher.publish(cmd)
        self.get_logger().info(f"Published motion for: {text}")

        # cancel previous timer if active
        if self.stop_timer is not None:
            self.stop_timer.cancel()

        # create stop timer
        if duration > 0:
            self.stop_timer = self.create_timer(duration, self.stop_robot)

    def stop_robot(self):
        stop = Twist()
        self.publisher.publish(stop)
        self.get_logger().info("Stopped robot")

        if self.stop_timer is not None:
            self.stop_timer.cancel()
            self.stop_timer = None


def main():
    rclpy.init()
    node = VoiceMotion()
    rclpy.spin(node)


if __name__ == '__main__':
    main()