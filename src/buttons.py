import pygame
from pygame.locals import *
from appModel import AppState, AppModel


class Button(pygame.Rect):
    def __init__(self, left, top, width, height, text, color):
        super().__init__(left, top, width, height)
        self.color = color
        self.text = text
        self.corner_radius = 5

    def isClicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.collidepoint(event.pos):
                return True

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self, border_radius=self.corner_radius)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.center)
        screen.blit(text, text_rect)


class ToggleButton(Button):
    def __init__(self, left, top, width, height, text, color, toState):
        super().__init__(left, top, width, height, text, color)
        self.selfState = toState

    def isClicked(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.collidepoint(event.pos):
                return True
        return False

    def update(self, event, appModel: AppModel):
        if self.isClicked(event):
            if appModel.state != self.selfState:
                appModel.setState(self.selfState)
            else:
                appModel.setState(AppState.idle)

    def setState(self, pressed: bool):
        self.pressedDown = pressed

    def draw(self, screen, appModel: AppModel):
        r = self.corner_radius
        brightnessIncrement = 100
        if appModel.state == self.selfState:
            pygame.draw.rect(
                screen,
                (
                    self.color[0] + brightnessIncrement,
                    self.color[1] + brightnessIncrement,
                    self.color[2] + brightnessIncrement,
                ),
                self,
                border_radius=r,
            )
        else:
            pygame.draw.rect(screen, self.color, self, border_radius=r)
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255, 255, 255))
        text_rect = text.get_rect(center=self.center)
        screen.blit(text, text_rect)
