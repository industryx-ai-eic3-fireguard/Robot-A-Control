[README.md](https://github.com/user-attachments/files/34297821/README.md)
# robot_a_control : Programmation du Robot A (Préhension)

**Auteur : Youvens Appolon**
**Projet :** INDUSTRY-X AI (EIC 3.0) | **Équipe :** FIREGUARD-X
**Rôle :** Programmation du Robot A (pick & place)

## Description

Ce paquet ROS 2 (Jazzy) contient la programmation du **Robot A**, le bras
manipulateur chargé de saisir les objets sur le convoyeur et de les déposer
à un emplacement donné, dans la simulation Gazebo Harmonic.

Le robot a **3 articulations rotoïdes** (`joint_1` base, `joint_2` épaule,
`joint_3` coude) et une **pince** (`joint_finger_left`, prismatique). Son modèle
(`robot_a.urdf`) est fourni par Emmanuel Remy ; ce paquet en reprend les
dimensions et les limites articulaires.

Le code calcule le mouvement du bras puis publie des commandes de position
sur des topics ROS 2. Le cycle complet est :

`home -> au-dessus de l'objet -> descente -> fermeture pince -> remontée
-> au-dessus du dépôt -> descente -> ouverture pince -> remontée -> home`

## Principe de conception

Le code est séparé en couches : les mathématiques n'ont **aucune dépendance
à ROS**, ce qui permet de les tester sur n'importe quel ordinateur, sans
Gazebo.

| Fichier | Rôle | Dépend de ROS ? |
|---|---|---|
| `config.py` | Dimensions du bras, limites, positions pick/place, topics | Non |
| `kinematics.py` | Cinématique directe `forward` et inverse `inverse` | Non |
| `trajectory.py` | Interpolation douce entre configurations (profil 3s²-2s³) | Non |
| `pick_sequence.py` | Construit la séquence pick & place à partir des positions | Non |
| `pick_node.py` | Nœud ROS 2 : publie les commandes d'articulations | **Oui** |
| `test/test_kinematics.py` | Tests automatiques (pytest) | Non |
| `tools/plot_arm.py` | Trace le bras et la trajectoire en 3D (matplotlib) | Non |
| `launch/pick.launch.py` | Lance le nœud | Oui |

## Cinématique en bref

- `q1 = atan2(y, x)` oriente le bras vers la cible.
- Le reste est un problème plan à 2 liens, résolu avec la loi des cosinus :
  `cos(q3) = (D² - L2² - L3²) / (2·L2·L3)`.
- Deux solutions existent (coude haut / bas) ; on garde celle qui respecte
  les limites de l'URDF. Si aucune n'existe, la cible est hors de portée.

## Installation et tests (sans ROS)

```bash
pip install pytest matplotlib
python3 -m pytest -q            # tests de cinématique et de trajectoire
python3 tools/plot_arm.py       # génère arm_plot.png
```

## Utilisation avec ROS 2 Jazzy

```bash
# depuis le workspace (ex. ~/ros2_ws), le paquet dans src/
colcon build --packages-select robot_a_control
source install/setup.bash

ros2 run robot_a_control pick_node
# ou : ros2 launch robot_a_control pick.launch.py

# Lancer un pick sur une position (x, y, z en mètres, repère de la base)
ros2 topic pub --once /robot_a/target_object geometry_msgs/msg/Point \
  "{x: 0.55, y: 0.0, z: 0.15}"
```

Pour lancer automatiquement un cycle au démarrage :
`ros2 run robot_a_control pick_node --ros-args -p auto_start:=true`

## Interface avec les autres membres

| Élément | Fourni par | Où le régler |
|---|---|---|
| Modèle URDF, topics de commande des articulations | Emmanuel Remy | `JOINT_CMD_TOPICS`, dimensions dans `config.py` |
| Position du convoyeur et des objets (monde Gazebo) | Dany Badio | `PICK_POS`, `PLACE_POS` dans `config.py` |
| Dépôt GitHub | Stecy Carla Saint-Prévil | `robot_a_control/` à placer dans le dépôt du groupe |

Commandes publiées : `std_msgs/Float64`, une commande de **position** (rad,
ou m pour la pince) par articulation :

- `/robot_a/joint_1/cmd_pos`, `/robot_a/joint_2/cmd_pos`, `/robot_a/joint_3/cmd_pos`
- `/robot_a/joint_finger_left/cmd_pos` (0.0 = ouverte, 0.03 = fermée)

## Limites connues

- **Valeurs provisoires :** les positions pick/place et les noms de topics
  dans `config.py` sont des valeurs par défaut à confirmer avec l'équipe.
- **Un seul doigt :** l'URDF actuel n'a que `finger_left`. Un second doigt est
  nécessaire pour saisir réellement un objet.
- **Orientation de la pince non contrôlée :** avec 3 articulations, le bras
  atteint la position mais la pince reste inclinée.
- **Portée limitée :** à cause des limites de `joint_3`, la cible doit se
  trouver entre environ 0.53 m et 0.75 m de l'épaule.
- **Non testé dans Gazebo :** la partie ROS 2 doit être validée en simulation
  par un membre de l'équipe disposant du logiciel.

## Auteur

**Youvens Appolon**, responsable de la programmation du Robot A,
équipe FIREGUARD-X, INDUSTRY-X AI (EIC 3.0).
