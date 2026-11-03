"""kinematics.py - Cinématique directe et inverse du bras (maths pures, sans ROS).

Convention (déduite de l'URDF) :
  - joint_1 : rotation autour de Z (oriente le bras dans le plan XY)
  - joint_2, joint_3 : rotation autour de Y. Une rotation +q autour de Y
    fait pencher un lien vertical vers +x, donc la direction d'un lien
    est (sin(angle), cos(angle)) dans le plan (r, z), l'angle étant
    mesuré depuis la verticale.
  - q2 = angle du lien 2 ; q2 + q3 = angle du lien 3.
"""
import math
from . import config as C


def forward(q1, q2, q3):
    """Angles (rad) -> position (x, y, z) du bout de la pince."""
    r = C.L2 * math.sin(q2) + C.L3 * math.sin(q2 + q3)
    z = C.Z_SHOULDER + C.L2 * math.cos(q2) + C.L3 * math.cos(q2 + q3)
    return r * math.cos(q1), r * math.sin(q1), z


def _within_limits(q1, q2, q3):
    qs = {"joint_1": q1, "joint_2": q2, "joint_3": q3}
    for name, q in qs.items():
        lo, hi = C.JOINT_LIMITS[name]
        if not (lo + C.LIMIT_MARGIN <= q <= hi - C.LIMIT_MARGIN):
            return False
    return True


def inverse(x, y, z):
    """Position (x, y, z) -> (q1, q2, q3), ou None si inatteignable.

    Etapes :
      1. q1 = atan2(y, x)  : on tourne le bras vers la cible.
      2. On se ramène à un problème plan à 2 liens : r = sqrt(x²+y²),
         dz = z - Z_SHOULDER.
      3. Loi des cosinus : D² = L2² + L3² + 2·L2·L3·cos(q3)
      4. Deux solutions (coude +/-). On garde celle qui respecte les limites.
    """
    q1 = math.atan2(y, x)
    r = math.hypot(x, y)
    dz = z - C.Z_SHOULDER
    d2 = r * r + dz * dz

    cos_q3 = (d2 - C.L2 ** 2 - C.L3 ** 2) / (2 * C.L2 * C.L3)
    if abs(cos_q3) > 1.0:
        return None  # trop loin ou trop près

    phi = math.atan2(r, dz)  # angle de la cible depuis la verticale
    for sign in (1.0, -1.0):
        q3 = sign * math.acos(cos_q3)
        q2 = phi - math.atan2(C.L3 * math.sin(q3), C.L2 + C.L3 * math.cos(q3))
        if _within_limits(q1, q2, q3):
            return q1, q2, q3
    return None
