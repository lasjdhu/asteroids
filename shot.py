from typing import override

import pygame

from circleshape import CircleShape
from constants import SHOT_IMAGE_PATH, SHOT_RADIUS


class Shot(CircleShape):
    image: pygame.Surface | None = None

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, SHOT_RADIUS)
        self.position: pygame.Vector2

        if Shot.image is None:
            original_image = pygame.image.load(SHOT_IMAGE_PATH).convert_alpha()
            size = int(SHOT_RADIUS * 2)
            Shot.image = pygame.transform.scale(original_image, (size, size))

    @override
    def draw(self, screen: pygame.Surface) -> None:
        if Shot.image is None:
            return

        rect = Shot.image.get_rect(center=self.position)
        screen.blit(Shot.image, rect)

    @override
    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
