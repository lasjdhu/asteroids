import random
from typing import override

import pygame

from src.constants import (
    ASTEROID_DEBRIS_MAX_COUNT,
    ASTEROID_DEBRIS_MAX_LIFETIME,
    ASTEROID_DEBRIS_MAX_ROTATION_SPEED,
    ASTEROID_DEBRIS_MAX_SIZE,
    ASTEROID_DEBRIS_MAX_SPEED,
    ASTEROID_DEBRIS_MIN_COUNT,
    ASTEROID_DEBRIS_MIN_LIFETIME,
    ASTEROID_DEBRIS_MIN_SIZE,
    ASTEROID_DEBRIS_MIN_SPEED,
)


class AsteroidDebris(pygame.sprite.Sprite):
    """A tiny, short-lived asteroid sprite emitted when an asteroid is hit."""

    containers: tuple[pygame.sprite.Group, ...]

    def __init__(
        self,
        position: pygame.Vector2,
        parent_velocity: pygame.Vector2,
        source_image: pygame.Surface,
    ) -> None:
        super().__init__(*self.containers)
        self.position = position.copy()

        size = random.randint(ASTEROID_DEBRIS_MIN_SIZE, ASTEROID_DEBRIS_MAX_SIZE)
        self.image = pygame.transform.smoothscale(source_image, (size, size))
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(
            -ASTEROID_DEBRIS_MAX_ROTATION_SPEED,
            ASTEROID_DEBRIS_MAX_ROTATION_SPEED,
        )

        direction = pygame.Vector2(1, 0).rotate(random.uniform(0, 360))
        speed = random.uniform(ASTEROID_DEBRIS_MIN_SPEED, ASTEROID_DEBRIS_MAX_SPEED)
        self.velocity = parent_velocity * 0.25 + direction * speed
        self.lifetime = random.uniform(
            ASTEROID_DEBRIS_MIN_LIFETIME, ASTEROID_DEBRIS_MAX_LIFETIME
        )
        self.age = 0.0

    @classmethod
    def burst(
        cls,
        position: pygame.Vector2,
        parent_velocity: pygame.Vector2,
        source_image: pygame.Surface,
    ) -> None:
        for _ in range(
            random.randint(ASTEROID_DEBRIS_MIN_COUNT, ASTEROID_DEBRIS_MAX_COUNT)
        ):
            cls(position, parent_velocity, source_image)

    @override
    def update(self, dt: float) -> None:
        self.age += dt
        if self.age >= self.lifetime:
            self.kill()
            return

        self.position += self.velocity * dt
        self.rotation = (self.rotation + self.rotation_speed * dt) % 360

    def draw(self, screen: pygame.Surface) -> None:
        alpha = round(255 * (1 - self.age / self.lifetime))
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        rotated_image.set_alpha(alpha)
        rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, rect)
