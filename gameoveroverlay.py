import pygame

from constants import (
    FONT_PATH,
    GAME_OVER_APPEAR_DURATION,
    GAME_OVER_BAND_COLOR,
    GAME_OVER_BAND_HEIGHT,
    GAME_OVER_DISAPPEAR_DURATION,
    GAME_OVER_DURATION,
    GAME_OVER_FONT_SIZE,
    GAME_OVER_SHADE_COLOR,
    GAME_OVER_TEXT_COLOR,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)


class GameOverOverlay:
    def __init__(self) -> None:
        self.font = pygame.font.Font(FONT_PATH, GAME_OVER_FONT_SIZE)
        self.elapsed = 0.0

    def reset(self) -> None:
        self.elapsed = 0.0

    def update(self, dt: float) -> None:
        self.elapsed += dt

    def is_finished(self) -> bool:
        return self.elapsed >= GAME_OVER_DURATION

    def draw(self, screen: pygame.Surface) -> None:
        appear = min(1.0, self.elapsed / GAME_OVER_APPEAR_DURATION)
        disappear = min(
            1.0,
            max(
                0.0,
                (GAME_OVER_DURATION - self.elapsed) / GAME_OVER_DISAPPEAR_DURATION,
            ),
        )
        visibility = appear * disappear

        shade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        shade.fill((*GAME_OVER_SHADE_COLOR, int(175 * appear)))
        screen.blit(shade, (0, 0))

        band = pygame.Surface((SCREEN_WIDTH, GAME_OVER_BAND_HEIGHT), pygame.SRCALPHA)
        band.fill((*GAME_OVER_BAND_COLOR, int(190 * visibility)))
        screen.blit(band, (0, SCREEN_HEIGHT // 2 - GAME_OVER_BAND_HEIGHT // 2))

        text = self.font.render("GAME OVER", False, GAME_OVER_TEXT_COLOR)
        text = pygame.transform.scale_by(text, appear)
        text.set_alpha(int(255 * visibility))
        screen.blit(
            text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        )
