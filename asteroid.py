import os
import random
from typing import override

import pygame

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS
from logger import log_event


class Asteroid(CircleShape):
    images: list[pygame.Surface] = []

    def __init__(self, x: float, y: float, radius: float) -> None:
        super().__init__(x, y, radius)
        self.position: pygame.Vector2
        self.rotation: float = random.uniform(0, 360)
        self.rotation_speed: float = random.uniform(-45, 45)

        if len(Asteroid.images) == 0:
            Asteroid.images = [
                pygame.image.load(os.path.join("assets/images", "asteroid1.png")).convert_alpha(),
                pygame.image.load(os.path.join("assets/images", "asteroid2.png")).convert_alpha(),
                pygame.image.load(os.path.join("assets/images", "asteroid3.png")).convert_alpha(),
            ]

        original_image = random.choice(Asteroid.images)
        size = int(self.radius * 2)
        self.image = pygame.transform.scale(original_image, (size, size))

    @override
    def draw(self, screen: pygame.Surface) -> None:
        rotated_image = pygame.transform.rotozoom(self.image, self.rotation, 1.0)
        rect = rotated_image.get_rect(center=self.position)
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

        angle = random.uniform(20, 50)
        new_r = self.radius - ASTEROID_MIN_RADIUS

        first_asteroid = Asteroid(self.position.x, self.position.y, new_r)
        second_asteroid = Asteroid(self.position.x, self.position.y, new_r)

        first_asteroid.velocity = self.velocity.rotate(angle) * 1.2
        second_asteroid.velocity = self.velocity.rotate(-angle) * 1.2