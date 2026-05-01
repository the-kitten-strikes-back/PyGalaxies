# 🌌 PyGalaxies

> *Watch celestial bodies collide and implode.*

A real-time interactive galaxy simulator built with Python and Pygame. Models galaxies with thousands of stars, realistic gravity with softening, collisions, mergers, and core accretion—all in stunning real-time.

---

## 🎯 Features

- **Real-time N-body gravity simulation** - Softening parameter and collision handling
- **Core formation & accretion** - Realistic physics for stellar accumulation
- **Dynamic galaxy spawning** - Generate and add new galaxies on demand
- **Interactive camera** - Zoom, pan, and explore at any scale
- **Star trails** - Visual history of stellar movement (toggleable)
- **Simulation speed control** - Speed up, slow down, or pause
- **Live HUD** - Real-time statistics, FPS, and control display
- **Thousands of bodies** - Configurable max star count for performance tuning

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pygame
- numpy

### Installation

```bash
pip install pygame numpy

git clone https://github.com/the-kitten-strikes-back/PyGalaxies.git
cd PyGalaxies
python main.py
```

---

## 🎮 Controls

| Key(s) | Action |
|--------|--------|
| `SPACE` | Pause/unpause simulation |
| `R` | Reset scene |
| `G` | Add a new galaxy |
| `T` | Toggle star trails |
| `[` / `]` | Decrease/increase simulation speed |
| `+` / `-` | Zoom in/out |
| `WASD` or Arrow Keys | Pan camera |
| Mouse Wheel | Zoom |

---

## ⚙️ Configuration

Customize simulation behavior via the `SimConfig` class in `main.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `width` | 1280 | Window width in pixels |
| `height` | 840 | Window height in pixels |
| `fps` | 60 | Target frames per second |
| `g` | 26.0 | Gravitational constant (scaled) |
| `dt` | 0.012 | Simulation timestep |
| `softening` | 7.0 | Softening parameter for gravity |
| `max_stars` | 2200 | Maximum number of bodies |
| `default_star_count` | 750 | Stars per spawned galaxy |
| `trail_alpha` | 28 | Opacity of star trails (0-255) |
| `collision_distance_factor` | 0.95 | Collision threshold multiplier |
| `core_accretion_scale` | 4.2 | Core accretion radius scale |
| `min_accretion_radius` | 10.0 | Minimum accretion radius |

---

## 🔬 Physics Engine

**Gravitational Softening:**
Prevents singularities and improves stability with very close bodies.

**Collision Detection:**
Stars merge when they pass within the collision threshold, creating more massive bodies.

**Core Accretion:**
Stellar cores grow by absorbing nearby material, creating realistic galaxy centers.

---

## 💡 Tips

- Start with **default settings** to explore basic galaxy collisions.
- **Increase `max_stars`** for more detailed simulations (impacts FPS).
- **Adjust `softening`** to change how gravitational interactions feel.
- **Reduce `g`** for slower, more stable galaxy formations.
- **Toggle trails** (`T`) to see stellar orbital history.

---

## 🛠️ Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-darkgreen?style=flat)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white)

---

## 📜 License

Created by **The Kitten**. Free to explore, modify, and share.

---

*N-body simulation · Astrophysics · Real-time visualization*
