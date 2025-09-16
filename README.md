# Requiem for an Immortal Death

> Un projet de jeu 2D utilisant Pygame.

![Status](https://img.shields.io/badge/status-WIP-orange) ![OS](https://img.shields.io/badge/OS-Windows%20%7C%20macOS-blue)

## Table des matières

-   [Présentation](#présentation)
-   [Stack et compatibilité](#stack-et-compatibilité)
-   [Installation](#installation)
-   [Exécution](#exécution)
-   [Contrôles](#contrôles)
-   [Système d'input reconfigurable](#système-dinput-reconfigurable)
-   [Structure du projet](#structure-du-projet)
-   [Contenu et assets](#contenu-et-assets)
-   [Fonctionnalités actuelles](#fonctionnalités-actuelles)
-   [Roadmap](#roadmap)
-   [Licence et crédits](#licence-et-crédits)

## Présentation

Requiem for an Immortal Death est un jeu 2D en développement. Objectif: exploration et mise en place d’une base technique (chargement de cartes TMX, caméra, entité joueur, boucle de jeu) pour évoluer vers un jeu plus complet.

## Stack et compatibilité

-   Python: 3.13.5
-   OS: Windows, macOS
-   Principaux packages (voir `requirements.txt`):
    -   pygame==2.6.1
    -   pyscroll==2.31
    -   PyTMX==3.32
-   Cartes: format TMX (Tiled). Pas de version Tiled spécifique requise documentée pour l’instant.

## Installation

Recommandé: environnement virtuel Python standard.

```bash
# Créer l'environnement virtuel (macOS/Linux)
python3 -m venv .venv
source .venv/bin/activate

# Windows PowerShell
# py -3 -m venv .venv
# .venv\\Scripts\\Activate.ps1

# Dépendances
pip install -r requirements.txt
```

Aucune dépendance système supplémentaire n’est requise pour le moment.

## Exécution

```bash
python main.py
```

-   Aucun argument/flag optionnel pour l’instant.
-   Affichage actuel: fenêtre 1280x720 (voir `screen.py`). Le plein écran pourra être ajouté ultérieurement.

## Contrôles

Extraits du code (`entity.py`) — support des flèches et du mapping AZERTY ZQSD:

| Action         | Touche(s)        |
| -------------- | ---------------- |
| Aller à droite | Flèche droite, D |
| Aller à gauche | Flèche gauche, Q |
| Aller en bas   | Flèche bas, S    |
| Aller en haut  | Flèche haut, Z   |
| Sprint         | Left Shift       |

Remarques:

-   Pas (encore) de touches dédiées pour Pause/Menu ou Inventaire.
-   Le déplacement est exclusif (pas de diagonales simultanées).

## Système d'input reconfigurable

Les contrôles sont définis au niveau d’actions (ex: `move_left`, `sprint`) et sont reconfigurables via un fichier JSON.

- Fichier: `config/controls.json`
- Profil par défaut: `default` (AZERTY + flèches)
- Exemple de structure:

```json
{
  "version": 1,
  "profiles": {
    "default": {
      "move_left": ["K_LEFT", "K_q"],
      "move_right": ["K_RIGHT", "K_d"],
      "move_up": ["K_UP", "K_z"],
      "move_down": ["K_DOWN", "K_s"],
      "sprint": ["K_LSHIFT"],
      "pause": ["K_ESCAPE"]
    }
  },
  "active_profile": "default"
}
```

Pour rebind via code:

```python
from input_manager import InputManager
im = InputManager()
im.rebind("pause", ["K_p", "K_ESCAPE"])  # remappe l'action "pause"
im.save()  # persiste dans config/controls.json
```

L’entité (`entity.py`) lit les actions via `InputManager` (et non plus les touches brutes), ce qui facilite les rebindings et les profils.

## Structure du projet

-   `main.py`: point d’entrée, importe depuis le package `src/` et lance la boucle de jeu.
-   `src/`: code applicatif
    -   `src/game.py`: contrôleur principal (boucle) et gestion d’états (state machine).
    -   `src/screen.py`: fenêtre Pygame, timing, FPS, calcule `dt` par frame.
    -   `src/map.py`: gestion de la carte TMX (PyTMX + Pyscroll), méthodes `update(dt)` et `render(...)`.
    -   `src/entity.py`: entité joueur (sprite, déplacement, sprint, orientation). Mouvement à `dt` constant et diagonales normalisées.
    -   `src/input_manager.py`: système d’input reconfigurable (actions) avec persistance JSON.
    -   `src/tools.py`: utilitaires communs (spritesheets, etc.).
    -   `src/states/`: états du jeu
        -   `src/states/base_state.py`: classe de base abstraite pour les états.
        -   `src/states/play_state.py`: état de jeu principal.
-   `assets/`: ressources du jeu
    -   `assets/maps/`: cartes `.tmx`
    -   `assets/tiles/`: tilesets
    -   `assets/sprites/`: sprites (ex: `player.png`)
-   `config/`: fichiers de configuration
    -   `config/controls.json`: bindings des actions

## Contenu et assets

-   Format cartes: TMX (Tiled).
-   Rendu: Pyscroll avec zoom caméra (voir `map.py`, `map_layer.zoom = 3`).
-   Crédits assets et histoire/graphisme: Maxime.
-   Développement: Gary, Ulysse.

## Fonctionnalités actuelles

-   Chargement d’une carte TMX (`assets/maps/map0.tmx`).
-   Rendu défilant avec Pyscroll et caméra centrée sur le joueur.
-   Entité joueur avec déplacement (flèches et ZQSD) et sprint (Left Shift).
-   Boucle de jeu Pygame avec capping à 60 FPS.
-   Mouvement indépendant du framerate via `dt`.
-   Système d’inputs reconfigurable (JSON) par actions.
-   Système d’états minimal (`states/`) pour préparer menus et pauses.
-   Chemins robustes via `pathlib` pour assets/et configs.

## Roadmap

La feuille de route détaillée est maintenue dans [`toto.md`](./toto.md). Cochez les cases au fur et à mesure de l’avancement.

Points notables à venir (extrait):

-   Menu in-game, inventaire, sauvegardes, paramètres, rebindings des touches.
-   Système audio, architecture d’états, UI/UX de base.
-   Tutoriel, quêtes, IA NPC, physique avancée, combat, mini-map, etc.

## Licence et crédits

-   Licence: All rights reserved.
-   Crédits:
    -   Histoire et graphisme: Maxime
    -   Développement: Gary, Ulysse
-   Contact: non communiqué

---

Projet en cours (WIP)
