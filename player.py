import os
from typing import override

import pygame

from circleshape import CircleShape
from shot import Shot
from constants import (
    PLAYER_RADIUS,
    PLAYER_SCALE,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
)


class Player(CircleShape):
    frames: list[pygame.Surface] = []

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation: float = 0.0
        self.position: pygame.Vector2
        self.timer: float = 0.0

        if len(Player.frames) == 0:
            img = pygame.image.load(os.path.join("assets/images", "player.png")).convert_alpha()
            frame_width = img.get_width() // 4
            frame_height = img.get_height()

            for i in range(4):
                frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
                frame = img.subsurface(frame_rect).copy()
                frame = pygame.transform.scale_by(frame, PLAYER_SCALE)
                Player.frames.append(frame)

        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.1

    @override
    def draw(self, screen: pygame.Surface) -> None:
        frame = Player.frames[self.current_frame]
        rotated_frame = pygame.transform.rotozoom(frame, -self.rotation, 1.0)
        rect = rotated_frame.get_rect(center=self.position)
        screen.blit(rotated_frame, rect)

    @override
    def update(self, dt: float) -> None:
        self.timer -= dt
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0.0
            self.current_frame = (self.current_frame + 1) % len(self.frames)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, -1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self) -> None:
        if self.timer > 0:
            return
        else:
            self.timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, -1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
