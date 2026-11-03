"""pick_node.py - Seul fichier qui connaît ROS 2.

Il appelle les modules de maths et publie les commandes.
Une minuterie (timer) envoie un point de la trajectoire à chaque tick,
donc le nœud ne bloque jamais.
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from geometry_msgs.msg import Point

from . import config as C
from .trajectory import build_path
from .pick_sequence import build_pick_place, Unreachable

ORDER = ["joint_1", "joint_2", "joint_3", "joint_finger_left"]


class PickNode(Node):
    def __init__(self):
        super().__init__("robot_a_pick_node")

        self.declare_parameter("auto_start", False)
        self.pubs = {
            name: self.create_publisher(Float64, topic, 10)
            for name, topic in C.JOINT_CMD_TOPICS.items()
        }
        self.create_subscription(Point, C.TARGET_TOPIC, self.on_target, 10)
        self.timer = self.create_timer(1.0 / C.RATE_HZ, self.tick)
        self.path = []   # points à envoyer
        self.index = 0

        if self.get_parameter("auto_start").value:
            self.start_cycle(C.PICK_POS)
        self.get_logger().info("Noeud prêt. Publie un Point sur "
                               f"{C.TARGET_TOPIC} pour lancer un pick.")

    def on_target(self, msg):
        if self.index < len(self.path):
            self.get_logger().warn("Mouvement en cours, cible ignorée.")
            return
        self.start_cycle((msg.x, msg.y, msg.z))

    def start_cycle(self, pick_pos):
        try:
            waypoints = build_pick_place(pick=pick_pos)
        except Unreachable as e:
            self.get_logger().error(str(e))
            return
        self.path = build_path(waypoints, C.RATE_HZ)
        self.index = 0
        self.get_logger().info(f"Cycle lancé ({len(self.path)} points).")

    def tick(self):
        if self.index >= len(self.path):
            return
        point = self.path[self.index]
        for name, value in zip(ORDER, point):
            self.pubs[name].publish(Float64(data=float(value)))
        self.index += 1
        if self.index == len(self.path):
            self.get_logger().info("Cycle terminé.")


def main(args=None):
    rclpy.init(args=args)
    node = PickNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
