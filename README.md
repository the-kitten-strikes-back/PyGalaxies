# Watch celestial bodies collide and implode.

# PyGalaxies

**PyGalaxies** is a real-time interactive galaxy simulator built with **Python** and **Pygame**.

It models galaxies with thousands of stars, realistic gravity, collisions, mergers, and core accretion.

---

## Features

- Real-time N-body gravity simulation with softening and collision handling
- Core formation and accretion physics
- Dynamic galaxy spawning
- Adjustable zoom and camera pan
- Toggleable star trails
- Simulation speed control
- On-screen HUD displaying statistics and controls

---

## Installation

**Requirements:**

- Python 3.x
- pygame
- numpy

Install dependencies with:

```bash
pip install pygame numpy
```

---

## Running the Simulator

Clone the repository and run:

```bash
git clone https://github.com/the-kitten-strikes-back/PyGalaxies.git
cd PyGalaxies
python main.py
```

Use the controls below to explore and interact with galaxies in real-time.

---

## Configuration

Simulation behavior can be customized via the `SimConfig` class in `main.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `width` | 1280 | Window width in pixels |
| `height` | 840 | Window height in pixels |
| `fps` | 60 | Target frames per second |
| `g` | 26.0 | Gravitational constant (scaled) |
| `dt` | 0.012 | Simulation timestep |
| `softening` | 7.0 | Softening parameter for gravity |
| `max_stars` | 2200 | Maximum number of bodies in simulation |
| `default_star_count` | 750 | Stars per spawned galaxy |
| `trail_alpha` | 28 | Opacity of star trails (0-255) |
| `collision_distance_factor` | 0.95 | Collision threshold multiplier |
| `core_accretion_scale` | 4.2 | Core accretion radius scale |
| `min_accretion_radius` | 10.0 | Minimum accretion radius |

---

## Controls

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

## License

Created by **The Kitten**. Free to explore, modify, and share.