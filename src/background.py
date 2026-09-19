import math
import random

import pygame


class Background:
    def __init__(self, width: int, height: int, star_count: int = 160) -> None:
        self.width = width
        self.height = height
        self.gradient = self._create_gradient()
        self.time = 0.0

        self.stars: list[dict[str, float]] = []
        for _ in range(star_count):
            self.stars.append(
                {
                    "x": random.uniform(0, width),
                    "y": random.uniform(0, height),
                    "radius": random.choice([1.0, 1.0, 1.0, 1.5, 2.0]),
                    "base_alpha": random.uniform(45, 130),
                    "flicker_speed": random.uniform(1.5, 5.0),
                    "flicker_offset": random.uniform(0, math.tau),
                }
            )

    def _create_gradient(self) -> pygame.Surface:
        surface = pygame.Surface((self.width, self.height)).convert()

        top_color = pygame.Color(3, 4, 12)
        middle_color = pygame.Color(18, 8, 30)
        bottom_color = pygame.Color(4, 24, 18)

        for y in range(self.height):
            progress = y / max(1, self.height - 1)

            if progress < 0.55:
                local_progress = progress / 0.55
                color = top_color.lerp(middle_color, local_progress)
            else:
                local_progress = (progress - 0.55) / 0.45
                color = middle_color.lerp(bottom_color, local_progress)

            pygame.draw.line(surface, color, (0, y), (self.width, y))

        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        for _ in range(18):
            x = random.randint(-100, self.width + 100)
            y = random.randint(-100, self.height + 100)
            radius = random.randint(120, 320)

            color = random.choice(
                [
                    (60, 25, 95, 10),
                    (25, 90, 65, 8),
                    (35, 20, 75, 9),
                ]
            )

            pygame.draw.circle(overlay, color, (x, y), radius)

        surface.blit(overlay, (0, 0))
        return surface

    def update(self, dt: float) -> None:
        self.time += dt

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.gradient, (0, 0))

        stars_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        for star in self.stars:
            flicker = math.sin(
                self.time * star["flicker_speed"] + star["flicker_offset"]
            )
            alpha = star["base_alpha"] + flicker * 45
            alpha = max(25, min(190, int(alpha)))

            pygame.draw.circle(
                stars_surface,
                (220, 245, 235, alpha),
                (int(star["x"]), int(star["y"])),
                star["radius"],
            )

        screen.blit(stars_surface, (0, 0))