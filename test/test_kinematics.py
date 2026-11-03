import random
from robot_a_control import kinematics as K, config as C
from robot_a_control.trajectory import interpolate, build_path
from robot_a_control.pick_sequence import build_pick_place


def test_forward_straight_up():
    x, y, z = K.forward(0, 0, 0)
    assert abs(x) < 1e-9 and abs(y) < 1e-9
    assert abs(z - (C.Z_SHOULDER + C.L2 + C.L3)) < 1e-9


def test_round_trip_ik_fk():
    """Aller-retour : angles -> position -> angles -> position."""
    random.seed(1)
    ok = 0
    for _ in range(500):
        q = (random.uniform(-3, 3), random.uniform(-1.4, 1.4), random.uniform(-1.4, 1.4))
        pos = K.forward(*q)
        sol = K.inverse(*pos)
        if sol is None:
            continue
        back = K.forward(*sol)
        assert all(abs(a - b) < 1e-6 for a, b in zip(pos, back))
        ok += 1
    assert ok > 50


def test_unreachable():
    assert K.inverse(3.0, 0.0, 0.5) is None


def test_trajectory_ends_exactly():
    pts = interpolate((0, 0, 0, 0), (1, 2, 3, 0.03), 1.0, 50)
    assert pts[-1] == (1, 2, 3, 0.03) and len(pts) == 50


def test_full_sequence_reachable():
    path = build_path(build_pick_place(), C.RATE_HZ)
    assert len(path) > 100
