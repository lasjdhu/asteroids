import sys
from typing import cast

import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_event, log_state
from player import Player


def main():
    _ = pygame.init()
    clock = pygame.time.Clock()
    dt = 0.0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    updatable: pygame.sprite.Group[CircleShape] = pygame.sprite.Group()
    drawable: pygame.sprite.Group[CircleShape] = pygame.sprite.Group()
    asteroids: pygame.sprite.Group[Asteroid] = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    _asteroid_field = AsteroidField()

    while True:
        log_state()
        _ = screen.fill("black")
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        updatable.update(dt)
        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")
                sys.exit()
        for sprite in drawable:
            drawable_sprite = cast(CircleShape, sprite)
            drawable_sprite.draw(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
