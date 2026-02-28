

---

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


## Controls


ActionKeyPause / ResumeSPACEReset SceneRSpawn GalaxyGToggle TrailsTDecrease Speed[Increase Speed]Zoom Out-Zoom In=Pan CameraW / A / S / D or Arrow KeysScroll ZoomMouse Wheel
---


## Installation


**Requirements:**


- Python 3.x
- pygame
- numpy


Install dependencies with:


```
Bashpip install pygame numpy
```


---


## Running the Simulator


Clone the repository and run:


```
Bashgit clone https://github.com/the-kitten-strikes-back/PyGalaxies.gitcd PyGalaxiespython main.py
```


Use the controls above to explore and interact with galaxies in real-time.


---


## Configuration


Simulation behavior can be customized via the `SimConfig` class:


SettingDescription`width`, `height`Window size`fps`Frame rate`g`Gravitational constant`dt`Simulation timestep`max_stars`Maximum number of stars`default_star_count`Default stars per galaxy`trail_alpha`Star trail opacity`collision_distance_factor`Collision sensitivity`core_accretion_scale`Core accretion radius multiplier`min_accretion_radius`Minimum radius for core accretion
---





## License


Created by **The Kitten**. Free to explore, modify, and share.


---





Do you want me to do that next?
