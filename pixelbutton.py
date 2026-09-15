import pygame

from constants import (
    BUTTON_SHADOW_OFFSET,
    BUTTON_SIZE,
    COLOR_BUTTON_BORDER_IDLE,
    COLOR_BUTTON_BORDER_SELECTED,
    COLOR_BUTTON_IDLE,
    COLOR_BUTTON_SELECTED,
    COLOR_BUTTON_SHADOW,
    COLOR_BUTTON_TEXT,
)


class PixelButton:
    def __init__(self, text: str, center: tuple[int, int]) -> None:
        self.text = text
        self.rect = pygame.Rect((0, 0), BUTTON_SIZE)
        self.rect.center = center

    def draw(
        self, screen: pygame.Surface, font: pygame.font.Font, selected: bool
    ) -> None:
        pygame.draw.rect(screen, COLOR_BUTTON_SHADOW, self.rect.move(BUTTON_SHADOW_OFFSET))
        fill = COLOR_BUTTON_SELECTED if selected else COLOR_BUTTON_IDLE
        border = COLOR_BUTTON_BORDER_SELECTED if selected else COLOR_BUTTON_BORDER_IDLE
        pygame.draw.rect(screen, fill, self.rect)
        pygame.draw.rect(screen, border, self.rect, 4)

        label = font.render(self.text, False, COLOR_BUTTON_TEXT)
        screen.blit(label, label.get_rect(center=self.rect.center))
