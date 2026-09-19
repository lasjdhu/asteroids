import pygame

from src.constants import (
    COLOR_CONTROL_TEXT,
    COLOR_TITLE,
    COLOR_TITLE_SHADOW,
    FONT_PATH,
    MENU_BUTTON_FONT_SIZE,
    MENU_CONTROLS_POSITION,
    MENU_EXIT_POSITION,
    MENU_FADE_DURATION,
    MENU_SMALL_FONT_SIZE,
    MENU_START_POSITION,
    MENU_TITLE_FONT_SIZE,
    MENU_TITLE_POSITION,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from src.pixelbutton import PixelButton


class StartScreen:
    def __init__(self) -> None:
        self.title_font = pygame.font.Font(FONT_PATH, MENU_TITLE_FONT_SIZE)
        self.button_font = pygame.font.Font(FONT_PATH, MENU_BUTTON_FONT_SIZE)
        self.small_font = pygame.font.Font(FONT_PATH, MENU_SMALL_FONT_SIZE)
        self.buttons = [
            PixelButton("START", MENU_START_POSITION),
            PixelButton("EXIT", MENU_EXIT_POSITION),
        ]
        self.selected_button = 0
        self.elapsed = 0.0

    def reset(self) -> None:
        self.selected_button = 0
        self.elapsed = 0.0

    def update(self, dt: float) -> None:
        self.elapsed += dt

    def handle_event(self, event: pygame.event.Event) -> str | None:
        if event.type == pygame.MOUSEMOTION:
            for index, button in enumerate(self.buttons):
                if button.rect.collidepoint(event.pos):
                    self.selected_button = index
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for index, button in enumerate(self.buttons):
                if button.rect.collidepoint(event.pos):
                    return "start" if index == 0 else "exit"
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_w):
                self.selected_button = (self.selected_button - 1) % len(self.buttons)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected_button = (self.selected_button + 1) % len(self.buttons)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return "start" if self.selected_button == 0 else "exit"
            elif event.key == pygame.K_ESCAPE:
                return "exit"
        return None

    def draw(self, screen: pygame.Surface) -> None:
        title_shadow = self.title_font.render("ASTEROIDS", False, COLOR_TITLE_SHADOW)
        title = self.title_font.render("ASTEROIDS", False, COLOR_TITLE)
        title_rect = title.get_rect(center=MENU_TITLE_POSITION)
        screen.blit(title_shadow, title_rect.move(6, 7))
        screen.blit(title, title_rect)

        for index, button in enumerate(self.buttons):
            button.draw(screen, self.button_font, index == self.selected_button)

        controls = self.small_font.render(
            "ARROWS OR WASD TO MOVE  /  SPACE TO FIRE",
            False,
            COLOR_CONTROL_TEXT,
        )
        screen.blit(controls, controls.get_rect(center=MENU_CONTROLS_POSITION))

        if self.elapsed < MENU_FADE_DURATION:
            fade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            fade.fill((0, 0, 0))
            fade.set_alpha(int(255 * (1.0 - self.elapsed / MENU_FADE_DURATION)))
            screen.blit(fade, (0, 0))
