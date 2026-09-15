import random
from typing import override

import pygame

from circleshape import CircleShape
from constants import (
    ASTEROID_IMAGE_PATHS,
    ASTEROID_MAX_ROTATION_SPEED,
    ASTEROID_MAX_SPLIT_ANGLE,
    ASTEROID_MIN_RADIUS,
    ASTEROID_MIN_ROTATION_SPEED,
    ASTEROID_MIN_SPLIT_ANGLE,
    ASTEROID_SPLIT_SPEED_MULTIPLIER,
)
from logger import log_event


class Asteroid(CircleShape):
    images: list[pygame.Surface] = []

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.position: pygame.Vector2
        self.rotation: float = random.uniform(0, 360)
        rotation_direction = random.choice((-1, 1))
        self.rotation_speed = rotation_direction * random.uniform(
            ASTEROID_MIN_ROTATION_SPEED, ASTEROID_MAX_ROTATION_SPEED
        )

        if len(Asteroid.images) == 0:
            Asteroid.images = [
                pygame.image.load(path).convert_alpha()
                for path in ASTEROID_IMAGE_PATHS
            ]

        original_image = random.choice(Asteroid.images)
        size = int(self.radius * 2)
        self.image = pygame.transform.scale(original_image, (size, size))

    @override
    def draw(self, screen: pygame.Surface) -> None:
        rotated_image = pygame.transform.rotate(self.image, self.rotation)
        render_position = (round(self.position.x), round(self.position.y))
        rect = rotated_image.get_rect(center=render_position)
        screen.blit(rotated_image, rect)

    @override
    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self.rotation = (self.rotation + self.rotation_speed * dt) % 360

    def split(self) -> None:
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")

        angle = random.uniform(ASTEROID_MIN_SPLIT_ANGLE, ASTEROID_MAX_SPLIT_ANGLE)
        new_r = self.radius - ASTEROID_MIN_RADIUS

        first_asteroid = Asteroid(self.position.x, self.position.y, new_r)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_r)

        first_asteroid.velocity = (
            self.velocity.rotate(angle) * ASTEROID_SPLIT_SPEED_MULTIPLIER
        )
        second_asteroid.velocity = (
            self.velocity.rotate(-angle) * ASTEROID_SPLIT_SPEED_MULTIPLIER
        )
