"""Trace le bras en 3D et la trajectoire de la pince (matplotlib).

Usage (depuis la racine du paquet) : python3 tools/plot_arm.py [--show]
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import matplotlib
if "--show" not in sys.argv:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
from robot_a_control import config as C, kinematics as K
from robot_a_control.trajectory import build_path
from robot_a_control.pick_sequence import build_pick_place


def arm_points(q1, q2, q3):
    """Points (base, épaule, coude, bout) en 3D."""
    c, s = math.cos(q1), math.sin(q1)
    r_e = C.L2 * math.sin(q2)
    z_e = C.Z_SHOULDER + C.L2 * math.cos(q2)
    return [(0, 0, 0), (0, 0, C.Z_SHOULDER), (r_e * c, r_e * s, z_e), K.forward(q1, q2, q3)]


path = build_path(build_pick_place(), C.RATE_HZ)
tips = [K.forward(*p[:3]) for p in path]

fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.plot(*zip(*tips), "--", color="gray", label="trajectoire")
n = len(path)
for i in (0, n // 5, 2 * n // 5, 3 * n // 5, 4 * n // 5):
    ax.plot(*zip(*arm_points(*path[i][:3])), "o-")
ax.scatter(*C.PICK_POS, c="green", s=80, label="pick")
ax.scatter(*C.PLACE_POS, c="red", s=80, label="place")
ax.set_xlabel("x"); ax.set_ylabel("y"); ax.set_zlabel("z"); ax.legend()
ax.set_box_aspect((1, 1, 1))
plt.savefig("arm_plot.png", dpi=100)
print("Image enregistrée : arm_plot.png")
if "--show" in sys.argv:
    plt.show()
