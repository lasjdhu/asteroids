import pygame

from asteroid import Asteroid
from asteroidfield import AsteroidField
from background import Background
from circleshape import CircleShape
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from gameoveroverlay import GameOverOverlay
from logger import log_event, log_state
from player import Player
from shot import Shot
from startscreen import StartScreen


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Asteroids")
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    background = Background(SCREEN_WIDTH, SCREEN_HEIGHT)
    start_screen = StartScreen()
    game_over_overlay = GameOverOverlay()

    updatable: pygame.sprite.Group[CircleShape] = pygame.sprite.Group()
    drawable: pygame.sprite.Group[CircleShape] = pygame.sprite.Group()
    asteroids: pygame.sprite.Group[Asteroid] = pygame.sprite.Group()
    shots: pygame.sprite.Group[Shot] = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    player: Player | None = None
    state = "menu"
    running = True

    def clear_game() -> None:
        nonlocal player
        for group in (updatable, drawable, asteroids, shots):
            group.empty()
        player = None

    def start_game() -> None:
        nonlocal player, state
        clear_game()
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        AsteroidField()
        state = "playing"
        log_event("game_started")

    while running:
        dt = clock.tick_busy_loop(60) / 1000
        background.update(dt)
        background.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif state == "menu":
                action = start_screen.handle_event(event)
                if action == "start":
                    start_game()
                elif action == "exit":
                    running = False
            elif state == "playing" and player is not None:
                player.handle_event(event)

        if state == "playing" and player is not None:
            log_state()
            updatable.update(dt)
            if any(player.collides_with(asteroid) for asteroid in asteroids):
                log_event("player_hit")
                game_over_overlay.reset()
                state = "game_over"
            else:
                for asteroid in asteroids:
                    for shot in shots:
                        if asteroid.collides_with(shot):
                            log_event("asteroid_shot")
                            shot.kill()
                            asteroid.split()

        if state in ("playing", "game_over"):
            for sprite in drawable:
                sprite.draw(screen)

        if state == "menu":
            start_screen.update(dt)
            start_screen.draw(screen)
        elif state == "game_over":
            game_over_overlay.update(dt)
            game_over_overlay.draw(screen)
            if game_over_overlay.is_finished():
                clear_game()
                start_screen.reset()
                state = "menu"

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
