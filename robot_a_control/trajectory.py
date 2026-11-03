"""trajectory.py - Génération de trajectoires (maths pures, sans ROS)."""


def smoothstep(s):
    """Profil 3s² - 2s³ : vitesse nulle au début et à la fin (pas de choc)."""
    return s * s * (3.0 - 2.0 * s)


def interpolate(start, end, duration, rate_hz):
    """Liste de points entre `start` et `end` (tuples de même taille).

    Le dernier point est exactement `end`.
    """
    n = max(1, int(round(duration * rate_hz)))
    points = []
    for i in range(1, n + 1):
        k = smoothstep(i / n)
        points.append(tuple(a + (b - a) * k for a, b in zip(start, end)))
    points[-1] = tuple(end)
    return points


def build_path(waypoints, rate_hz):
    """waypoints = [(config, durée), ...] -> liste continue de points.

    Chaque `config` est un tuple (q1, q2, q3, gripper). La durée est
    celle du segment qui ARRIVE à cette configuration.
    """
    path = []
    current = tuple(waypoints[0][0])
    path.append(current)
    for config, duration in waypoints[1:]:
        path.extend(interpolate(current, config, duration, rate_hz))
        current = tuple(config)
    return path
