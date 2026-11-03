"""pick_sequence.py - Construit la séquence pick & place (sans ROS)."""
from . import config as C
from .kinematics import inverse


class Unreachable(Exception):
    pass


def _ik(pos, label):
    sol = inverse(*pos)
    if sol is None:
        raise Unreachable(f"{label} {pos} est hors de portée ou hors limites")
    return sol


def build_pick_place(pick=C.PICK_POS, place=C.PLACE_POS):
    """Retourne [(config(q1,q2,q3,g), durée), ...] pour un cycle complet."""
    h = C.APPROACH_HEIGHT

    def above(p):
        return (p[0], p[1], p[2] + h)

    o, c = C.GRIPPER_OPEN, C.GRIPPER_CLOSED
    home = C.HOME_Q
    pre_pick = _ik(above(pick), "pre-pick")
    at_pick = _ik(pick, "pick")
    pre_place = _ik(above(place), "pre-place")
    at_place = _ik(place, "place")

    m, g = C.MOVE_DURATION, C.GRIPPER_DURATION
    return [
        ((*home, o), 0.0),            # départ
        ((*pre_pick, o), m),          # aller au-dessus de l'objet
        ((*at_pick, o), m),           # descendre
        ((*at_pick, c), g),           # fermer la pince
        ((*pre_pick, c), m),          # remonter avec l'objet
        ((*pre_place, c), m),         # aller au-dessus du dépôt
        ((*at_place, c), m),          # descendre
        ((*at_place, o), g),          # ouvrir la pince
        ((*pre_place, o), m),         # remonter
        ((*home, o), m),              # retour à la maison
    ]
