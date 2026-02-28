import math
from dataclasses import dataclass

import numpy as np
import pygame

#MADE BY THE KITTEN.
@dataclass
class SimConfig:
    width: int = 1280
    height: int = 840
    fps: int = 60
    g: float = 26.0 # scaled up obviously
    dt: float = 0.012
    softening: float = 7.0
    max_stars: int = 2200
    default_star_count: int = 750
    trail_alpha: int = 28
    collision_distance_factor: float = 0.95
    core_accretion_scale: float = 4.2
    min_accretion_radius: float = 10.0


class GalaxySimulator:
    def __init__(self, cfg: SimConfig):
        self.cfg = cfg
        pygame.init()
        pygame.display.set_caption("massive")
        self.screen = pygame.display.set_mode((cfg.width, cfg.height))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 16)

        self.positions = np.zeros((0, 2), dtype=np.float64)
        self.velocities = np.zeros((0, 2), dtype=np.float64)
        self.masses = np.zeros((0,), dtype=np.float64)
        self.radii = np.zeros((0,), dtype=np.float32)
        self.colors = np.zeros((0, 3), dtype=np.uint8)
        self.is_core = np.zeros((0,), dtype=bool)

        self.camera = np.array([0.0, 0.0], dtype=np.float64)
        self.zoom = 1.0
        self.time_scale = 1.0
        self.paused = False
        self.show_trails = True
        self.total_mergers = 0
        self.total_accretions = 0

        self.trail_layer = pygame.Surface((cfg.width, cfg.height), pygame.SRCALPHA)
        self.background = self._build_background()
        self.reset_scene()

    def _build_background(self) -> pygame.Surface:
        bg = pygame.Surface((self.cfg.width, self.cfg.height))
        for y in range(self.cfg.height):
            t = y / max(self.cfg.height - 1, 1)
            r = int(4 + 12 * t)
            g = int(8 + 18 * t)
            b = int(18 + 28 * t)
            pygame.draw.line(bg, (r, g, b), (0, y), (self.cfg.width, y))

        star_rng = np.random.default_rng(17)
        for _ in range(260):
            x = int(star_rng.integers(0, self.cfg.width))
            y = int(star_rng.integers(0, self.cfg.height))
            c = int(star_rng.integers(115, 190))
            bg.set_at((x, y), (c, c, c))
        return bg

    def reset_scene(self) -> None:
        self.positions = np.zeros((0, 2), dtype=np.float64)
        self.velocities = np.zeros((0, 2), dtype=np.float64)
        self.masses = np.zeros((0,), dtype=np.float64)
        self.radii = np.zeros((0,), dtype=np.float32)
        self.colors = np.zeros((0, 3), dtype=np.uint8)
        self.is_core = np.zeros((0,), dtype=bool)
        self.camera[:] = 0.0
        self.zoom = 1.0
        self.time_scale = 1.0
        self.paused = False
        self.total_mergers = 0
        self.total_accretions = 0
        self.trail_layer.fill((0, 0, 0, 0))

        self.spawn_galaxy(center=np.array([0.0, 0.0]), drift=np.array([0.0, 0.0]), spin=1.0)
        self.spawn_galaxy(center=np.array([640.0, -200.0]), drift=np.array([-8.8, 2.4]), spin=-1.0)

    def spawn_galaxy(
        self,
        center: np.ndarray,
        drift: np.ndarray,
        spin: float = 1.0,
        star_count: int | None = None,
        core_mass: float = 14000.0,
        disk_mass: float = 6200.0,
        radius: float = 280.0,
        arm_count: int = 4,
    ) -> None:
        if star_count is None:
            star_count = self.cfg.default_star_count
        if len(self.masses) + star_count + 1 > self.cfg.max_stars:
            return

        rng = np.random.default_rng()
        n = star_count + 1

        pos = np.zeros((n, 2), dtype=np.float64)
        vel = np.zeros((n, 2), dtype=np.float64)
        mass = np.zeros((n,), dtype=np.float64)
        rad = np.zeros((n,), dtype=np.float32)
        col = np.zeros((n, 3), dtype=np.uint8)
        core_flag = np.zeros((n,), dtype=bool)

        pos[0] = center
        vel[0] = drift
        mass[0] = core_mass
        rad[0] = 5.0
        col[0] = (255, 216, 145)
        core_flag[0] = True

        star_masses = rng.lognormal(mean=0.1, sigma=0.35, size=star_count)
        star_masses *= disk_mass / star_masses.sum()

        r = np.clip(rng.exponential(scale=radius * 0.42, size=star_count), 8.0, radius * 2.0)
        arms = rng.integers(0, arm_count, size=star_count)
        base_theta = (2.0 * math.pi * arms / arm_count) + rng.normal(0.0, 0.24, size=star_count)
        twist = spin * 2.7 * (r / radius)
        theta = base_theta + twist

        x = r * np.cos(theta)
        y = r * np.sin(theta)
        pos[1:, 0] = center[0] + x
        pos[1:, 1] = center[1] + y

        enclosed_disk_mass = disk_mass * (1.0 - np.exp(-r / (radius * 0.6)))
        enclosed_mass = core_mass + enclosed_disk_mass
        speed = np.sqrt(self.cfg.g * enclosed_mass / np.maximum(r, 1.0))

        tangent = np.stack((-np.sin(theta), np.cos(theta)), axis=1) * spin
        dispersion = rng.normal(0.0, 0.58, size=(star_count, 2))
        vel[1:] = drift + tangent * speed[:, None] + dispersion

        mass[1:] = star_masses
        rad[1:] = np.clip(0.9 + np.log1p(star_masses) * 0.65, 1.0, 2.7)

        temp = np.clip(rng.normal(0.6, 0.22, size=star_count), 0.0, 1.0)
        col[1:, 0] = (160 + temp * 95).astype(np.uint8)
        col[1:, 1] = (165 + temp * 70).astype(np.uint8)
        col[1:, 2] = (200 + (1.0 - temp) * 55).astype(np.uint8)

        self.positions = np.concatenate((self.positions, pos), axis=0)
        self.velocities = np.concatenate((self.velocities, vel), axis=0)
        self.masses = np.concatenate((self.masses, mass), axis=0)
        self.radii = np.concatenate((self.radii, rad), axis=0)
        self.colors = np.concatenate((self.colors, col), axis=0)
        self.is_core = np.concatenate((self.is_core, core_flag), axis=0)

    def _radius_from_mass(self, mass: float, core: bool) -> float:
        if core:
            return max(5.0, 2.4 + math.log1p(mass) * 0.55)
        return float(np.clip(0.9 + np.log1p(mass) * 0.65, 1.0, 4.0))

    def _merge_bodies(self, winner: int, loser: int) -> None:
        m1 = self.masses[winner]
        m2 = self.masses[loser]
        m_total = m1 + m2
        if m_total <= 0:
            return

        self.positions[winner] = (self.positions[winner] * m1 + self.positions[loser] * m2) / m_total
        self.velocities[winner] = (self.velocities[winner] * m1 + self.velocities[loser] * m2) / m_total
        self.masses[winner] = m_total

        became_core = bool(self.is_core[winner] or self.is_core[loser])
        self.is_core[winner] = became_core
        self.radii[winner] = self._radius_from_mass(m_total, core=became_core)
        if became_core:
            self.colors[winner] = (255, 216, 145)
        else:
            mixed = (self.colors[winner].astype(np.float64) * m1 + self.colors[loser].astype(np.float64) * m2) / m_total
            self.colors[winner] = np.clip(mixed, 0, 255).astype(np.uint8)

    def _resolve_collisions(self) -> None:
        n = len(self.masses)
        if n < 2:
            return

        cell_size = float(max(6.0, np.max(self.radii) * 2.5))
        cell_coords = np.floor(self.positions / cell_size).astype(np.int64)
        grid: dict[tuple[int, int], list[int]] = {}
        for idx, cell in enumerate(cell_coords):
            key = (int(cell[0]), int(cell[1]))
            grid.setdefault(key, []).append(idx)

        neighbor_offsets = (
            (-1, -1), (0, -1), (1, -1),
            (-1, 0), (0, 0), (1, 0),
            (-1, 1), (0, 1), (1, 1),
        )
        alive = np.ones(n, dtype=bool)
        merges = 0
        accretions = 0

        for i in range(n):
            if not alive[i]:
                continue

            cx, cy = int(cell_coords[i, 0]), int(cell_coords[i, 1])
            current_alive = True
            for ox, oy in neighbor_offsets:
                for j in grid.get((cx + ox, cy + oy), ()):
                    if j <= i or not alive[j] or not current_alive:
                        continue

                    delta = self.positions[j] - self.positions[i]
                    dist2 = float(delta[0] * delta[0] + delta[1] * delta[1])
                    if dist2 == 0.0:
                        dist2 = 1e-12

                    collision_dist = (self.radii[i] + self.radii[j]) * self.cfg.collision_distance_factor
                    collision_dist2 = collision_dist * collision_dist

                    core_idx = -1
                    if self.is_core[i]:
                        core_idx = i
                    elif self.is_core[j]:
                        core_idx = j

                    accretion_hit = False
                    if core_idx >= 0:
                        acc_radius = max(
                            self.cfg.min_accretion_radius,
                            float(self.radii[core_idx] * self.cfg.core_accretion_scale),
                        )
                        accretion_hit = dist2 <= acc_radius * acc_radius

                    if not accretion_hit and dist2 > collision_dist2:
                        continue

                    if self.is_core[i] and not self.is_core[j]:
                        winner, loser = i, j
                    elif self.is_core[j] and not self.is_core[i]:
                        winner, loser = j, i
                    elif self.masses[i] >= self.masses[j]:
                        winner, loser = i, j
                    else:
                        winner, loser = j, i

                    if not alive[winner] or not alive[loser]:
                        continue

                    core_interaction = bool(self.is_core[winner] or self.is_core[loser])
                    self._merge_bodies(winner, loser)
                    alive[loser] = False
                    merges += 1
                    if core_interaction:
                        accretions += 1

                    if loser == i:
                        current_alive = False
                        break
                if not current_alive:
                    break

        if merges == 0:
            return

        self.total_mergers += merges
        self.total_accretions += accretions
        self.positions = self.positions[alive]
        self.velocities = self.velocities[alive]
        self.masses = self.masses[alive]
        self.radii = self.radii[alive]
        self.colors = self.colors[alive]
        self.is_core = self.is_core[alive]

    def _compute_acceleration(self, pos: np.ndarray) -> np.ndarray:
        delta = pos[np.newaxis, :, :] - pos[:, np.newaxis, :]
        dist2 = np.sum(delta * delta, axis=2) + self.cfg.softening * self.cfg.softening
        np.fill_diagonal(dist2, np.inf)
        inv_dist3 = dist2 ** -1.5

        weighted = delta * self.masses[np.newaxis, :, np.newaxis]
        return self.cfg.g * np.sum(weighted * inv_dist3[:, :, np.newaxis], axis=1)

    def _step(self, dt: float) -> None:
        if len(self.masses) < 2:
            return

        acc_a = self._compute_acceleration(self.positions)
        self.velocities += 0.5 * acc_a * dt
        self.positions += self.velocities * dt
        acc_b = self._compute_acceleration(self.positions)
        self.velocities += 0.5 * acc_b * dt
        self._resolve_collisions()

    def _world_to_screen(self, world: np.ndarray) -> np.ndarray:
        return (world - self.camera) * self.zoom + np.array(
            [self.cfg.width * 0.5, self.cfg.height * 0.5], dtype=np.float64
        )

    def _draw_particles(self, target: pygame.Surface) -> None:
        pts = self._world_to_screen(self.positions)
        w = self.cfg.width
        h = self.cfg.height
        for i in range(len(pts)):
            x = int(pts[i, 0])
            y = int(pts[i, 1])
            if -4 <= x < w + 4 and -4 <= y < h + 4:
                radius = int(max(1, self.radii[i] * self.zoom))
                if self.is_core[i]:
                    radius = max(3, int(5 * self.zoom))
                pygame.draw.circle(target, tuple(int(v) for v in self.colors[i]), (x, y), radius)

    def _handle_input(self, dt_real: float) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.reset_scene()
                elif event.key == pygame.K_t:
                    self.show_trails = not self.show_trails
                    if not self.show_trails:
                        self.trail_layer.fill((0, 0, 0, 0))
                elif event.key == pygame.K_g:
                    angle = np.random.uniform(0, 2 * math.pi)
                    dist = np.random.uniform(500, 950)
                    center = np.array([math.cos(angle) * dist, math.sin(angle) * dist])
                    drift = np.array([-center[1], center[0]])
                    drift = drift / (np.linalg.norm(drift) + 1e-6) * np.random.uniform(4.0, 11.0)
                    self.spawn_galaxy(center=center, drift=drift, spin=np.random.choice([-1.0, 1.0]), star_count=380)
                elif event.key == pygame.K_LEFTBRACKET:
                    self.time_scale = max(0.2, self.time_scale * 0.8)
                elif event.key == pygame.K_RIGHTBRACKET:
                    self.time_scale = min(8.0, self.time_scale * 1.25)
                elif event.key == pygame.K_MINUS:
                    self.zoom = max(0.25, self.zoom * 0.9)
                elif event.key == pygame.K_EQUALS:
                    self.zoom = min(3.2, self.zoom * 1.1)
            if event.type == pygame.MOUSEWHEEL:
                self.zoom = float(np.clip(self.zoom * (1.0 + event.y * 0.09), 0.25, 3.2))

        keys = pygame.key.get_pressed()
        pan_speed = 450.0 / max(self.zoom, 0.1)
        move = np.zeros(2, dtype=np.float64)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move[0] -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move[0] += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move[1] -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move[1] += 1
        norm = np.linalg.norm(move)
        if norm > 0:
            self.camera += (move / norm) * pan_speed * dt_real
        return True

    def _draw_hud(self, fps_now: float) -> None:
        text_lines = [
            f"bodies: {len(self.masses)} / {self.cfg.max_stars}",
            f"fps: {fps_now:5.1f}",
            f"time scale: {self.time_scale:3.2f}x",
            f"zoom: {self.zoom:3.2f}x",
            f"mergers: {self.total_mergers}   accretions: {self.total_accretions}",
            "controls: SPACE pause  R reset  G add galaxy  T trails  [] speed  +/- zoom  WASD pan",
        ]
        y = 10
        for line in text_lines:
            img = self.font.render(line, True, (230, 236, 245))
            self.screen.blit(img, (10, y))
            y += 20

    def run(self) -> None:
        running = True
        while running:
            dt_real = self.clock.tick(self.cfg.fps) / 1000.0
            running = self._handle_input(dt_real)

            substeps = int(np.clip(1 + self.time_scale * 2.0, 1, 10))
            sim_dt = self.cfg.dt * self.time_scale / substeps
            if not self.paused:
                for _ in range(substeps):
                    self._step(sim_dt)

            self.screen.blit(self.background, (0, 0))
            if self.show_trails:
                self.trail_layer.fill((0, 0, 0, self.cfg.trail_alpha))
                self._draw_particles(self.trail_layer)
                self.screen.blit(self.trail_layer, (0, 0))
            else:
                self._draw_particles(self.screen)

            self._draw_hud(self.clock.get_fps())
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    GalaxySimulator(SimConfig()).run()
