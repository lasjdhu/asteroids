from typing import override

import pygame

from circleshape import CircleShape
from shot import Shot
from constants import (
    PLAYER_RADIUS,
    PLAYER_SCALE,
    PLAYER_ANIMATION_SPEED,
    PLAYER_IMAGE_PATH,
    PLAYER_SHOOT_COOLDOWN_SECONDS,
    PLAYER_SHOOT_SPEED,
    PLAYER_SPEED,
    PLAYER_TURN_SPEED,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHOT_RADIUS,
)


class Player(CircleShape):
    frames: list[pygame.Surface] = []

    def __init__(self, x: float, y: float) -> None:
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation: float = 0.0
        self.position: pygame.Vector2
        self.timer: float = 0.0
        self.pressed_keys: set[int] = set()

        if len(Player.frames) == 0:
            img = pygame.image.load(PLAYER_IMAGE_PATH).convert_alpha()
            frame_width = img.get_width() // 4
            frame_height = img.get_height()

            for i in range(4):
                frame_rect = pygame.Rect(i * frame_width, 0, frame_width, frame_height)
                frame = img.subsurface(frame_rect).copy()
                frame = pygame.transform.scale_by(frame, PLAYER_SCALE)
                Player.frames.append(frame)

        self.current_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = PLAYER_ANIMATION_SPEED

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

        if pygame.K_UP in self.pressed_keys:
            self.move(dt)
        if pygame.K_LEFT in self.pressed_keys:
            self.rotate(-dt)
        if pygame.K_DOWN in self.pressed_keys:
            self.move(-dt)
        if pygame.K_RIGHT in self.pressed_keys:
            self.rotate(dt)
        if pygame.K_SPACE in self.pressed_keys:
            self.shoot()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self.pressed_keys.add(event.key)
        elif event.type == pygame.KEYUP:
            self.pressed_keys.discard(event.key)
        elif event.type == pygame.WINDOWFOCUSLOST:
            self.pressed_keys.clear()

    def rotate(self, dt: float) -> None:
        self.rotation += PLAYER_TURN_SPEED * dt

    def triangle(self) -> tuple[pygame.Vector2, pygame.Vector2, pygame.Vector2]:
        forward = pygame.Vector2(0, -1).rotate(self.rotation)
        right = forward.rotate(90)
        return (
            self.position + forward * self.radius,
            self.position - forward * self.radius + right * self.radius,
            self.position - forward * self.radius - right * self.radius,
        )

    @override
    def collides_with(self, other: CircleShape) -> bool:
        vertices = self.triangle()
        center = other.position

        edge_crosses = []
        for start, end in zip(vertices, vertices[1:] + vertices[:1]):
            edge_crosses.append((end - start).cross(center - start))
        if all(cross >= 0 for cross in edge_crosses) or all(
            cross <= 0 for cross in edge_crosses
        ):
            return True

        radius_squared = other.radius * other.radius
        for start, end in zip(vertices, vertices[1:] + vertices[:1]):
            edge = end - start
            distance_along_edge = (center - start).dot(edge) / edge.length_squared()
            distance_along_edge = max(0.0, min(1.0, distance_along_edge))
            closest_point = start + edge * distance_along_edge
            if center.distance_squared_to(closest_point) <= radius_squared:
                return True

        return False

    def move(self, dt: float) -> None:
        unit_vector = pygame.Vector2(0, -1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        self.position.x = max(
            self.radius, min(self.position.x, SCREEN_WIDTH - self.radius)
        )
        self.position.y = max(
            self.radius, min(self.position.y, SCREEN_HEIGHT - self.radius)
        )

    def shoot(self) -> None:
        if self.timer > 0:
            return
        else:
            self.timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        direction = pygame.Vector2(0, -1).rotate(self.rotation)
        spawn_position = self.position + direction * (self.radius + SHOT_RADIUS)
        shot = Shot(spawn_position.x, spawn_position.y)
        shot.velocity = direction * PLAYER_SHOOT_SPEED
