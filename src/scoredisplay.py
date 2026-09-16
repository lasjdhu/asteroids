import pygame

from src.constants import (
    ASTEROID_MIN_RADIUS,
    FONT_PATH,
    SCORE_COLOR,
    SCORE_FONT_SIZE,
    SCORE_POSITION,
    SCORE_SHADOW_COLOR,
    SCORE_SHADOW_OFFSET,
)


class ScoreDisplay:
    def __init__(self) -> None:
        self.font = pygame.font.Font(FONT_PATH, SCORE_FONT_SIZE)
        self.score = 0

    def reset(self) -> None:
        self.score = 0

    def add_destroyed_asteroid(self, radius: float) -> None:
        if radius <= ASTEROID_MIN_RADIUS:
            self.score += 1

    def draw(self, screen: pygame.Surface) -> None:
        label = str(self.score)
        shadow = self.font.render(label, False, SCORE_SHADOW_COLOR)
        text = self.font.render(label, False, SCORE_COLOR)
        rect = text.get_rect(topright=SCORE_POSITION)
        screen.blit(shadow, rect.move(SCORE_SHADOW_OFFSET))
        screen.blit(text, rect)
