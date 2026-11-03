"""config.py (auteur : Youvens Appolon) - Toutes les constantes au même endroit.

Si Emmanuel (URDF) ou Dany (monde Gazebo) change une valeur,
on modifie UNIQUEMENT ce fichier.
"""

# ---------- Géométrie (copiée de robot_a.urdf) ----------
# joint_1 est à 0.05 (base) ; joint_2 est 0.2 plus haut dans shoulder_link
Z_SHOULDER = 0.05 + 0.2   # hauteur de l'axe de joint_2 (épaule) = 0.25 m
L2 = 0.4                  # upper_arm_link : joint_2 -> joint_3
# forearm_link : 0.3 m jusqu'à gripper_base, + ~0.05 m pour atteindre
# le bout des doigts (point de prise, TCP). A ajuster au besoin.
L3 = 0.3 + 0.05

# ---------- Limites articulaires (copiées de l'URDF) ----------
JOINT_LIMITS = {
    "joint_1": (-3.14, 3.14),
    "joint_2": (-1.57, 1.57),
    "joint_3": (-1.57, 1.57),
}
# Marge de sécurité pour ne pas viser exactement la butée
LIMIT_MARGIN = 0.02

# ---------- Pince (un seul doigt dans l'URDF actuel) ----------
# finger_left est à x=-0.04 et son axe est +x : 0.0 = ouvert, 0.03 = fermé
GRIPPER_OPEN = 0.0
GRIPPER_CLOSED = 0.03

# ---------- Positions dans le monde (PLACEHOLDERS) ----------
# A remplacer par les vraies valeurs de Dany BADIO (monde Gazebo).
# Repère = base du robot en (0,0,0). Unité = mètre.
PICK_POS = (0.55, 0.0, 0.15)     # objet sur le convoyeur
PLACE_POS = (0.0, 0.55, 0.15)    # où le déposer
APPROACH_HEIGHT = 0.15           # montée au-dessus de la cible (pre-pick, lift)

# ---------- Mouvement ----------
HOME_Q = (0.0, 0.0, 0.0)         # bras tout droit
RATE_HZ = 50.0                   # fréquence de publication des commandes
MOVE_DURATION = 2.0              # secondes par segment
GRIPPER_DURATION = 1.0           # secondes pour ouvrir / fermer

# ---------- Topics ROS 2 (PLACEHOLDERS, à confirmer avec Emmanuel) ----------
# Type std_msgs/Float64, une commande de position par articulation.
JOINT_CMD_TOPICS = {
    "joint_1": "/robot_a/joint_1/cmd_pos",
    "joint_2": "/robot_a/joint_2/cmd_pos",
    "joint_3": "/robot_a/joint_3/cmd_pos",
    "joint_finger_left": "/robot_a/joint_finger_left/cmd_pos",
}
TARGET_TOPIC = "/robot_a/target_object"   # geometry_msgs/Point (optionnel)
