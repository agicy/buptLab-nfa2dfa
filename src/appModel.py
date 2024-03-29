import pygame
from pygame.locals import *
import math
from enum import Enum
from pygame import gfxdraw


class AppState(Enum):
    idle = 0
    pairing = 1
    depairing = 2
    renamingLabels = 3
    removing = 4
    setAsStart = 5
    setAsEnd = 6
    renamingStates = 7


class AppModel:
    def __init__(self) -> None:
        self.state = AppState.idle
        self.selected_tiles: list[Tile] = []
        self.pressedKeys = []

    def setState(self, state: int):
        self.state = state
        self.selected_tiles.clear()
        self.pressedKeys.clear()


class TileType(Enum):
    start = 0
    final = 1
    intermediate = 2
    start_final = 3


class Tile(pygame.sprite.Sprite):
    def __init__(self, position, id):
        super().__init__()
        self.name = "q" + str(id)
        self.rect = pygame.Rect(position[0], position[1], 100, 100)
        self.rect.topleft = position
        self.clicked = False
        self.id = id
        self.type = TileType.intermediate

    def rename(self, id):
        self.id = id
        self.name = "q" + str(id)

    def isClicked(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                distance = math.sqrt(
                    (event.pos[0] - self.rect.centerx) ** 2
                    + (event.pos[1] - self.rect.centery) ** 2
                )
                if distance <= 50:
                    return True

    def update(self, event, appModel: AppModel):
        if self.isClicked(event):
            self.clicked = True
            if appModel.state != AppState.idle:
                appModel.selected_tiles.append(self)
            return True
        elif event.type == MOUSEBUTTONUP:
            self.clicked = False
        elif event.type == MOUSEMOTION:
            if self.clicked:
                self.rect.move_ip(event.rel)
        return False

    def draw(self, screen):
        backgroundColor = (125, 125, 125)

        gfxdraw.aacircle(
            screen,
            self.rect.centerx,
            self.rect.centery,
            50,
            (0, 0, 0),
        )

        if self.clicked:
            gfxdraw.filled_circle(
                screen,
                self.rect.centerx,
                self.rect.centery,
                50,
                (0, 0, 255),
            )
            gfxdraw.aacircle(
                screen,
                self.rect.centerx,
                self.rect.centery,
                50,
                (0, 0, 255),
            )
            gfxdraw.filled_circle(
                screen,
                self.rect.centerx,
                self.rect.centery,
                45,
                (255, 255, 255),
            )
            gfxdraw.aacircle(
                screen,
                self.rect.centerx,
                self.rect.centery,
                45,
                (255, 255, 255),
            )

        font = pygame.font.Font(None, 36)
        text = font.render(self.name, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)
        if self.type == TileType.final or self.type == TileType.start_final:
            pygame.draw.circle(screen, "black", self.rect.center, 40, 5)
        if self.type == TileType.start or self.type == TileType.start_final:
            arrow_x = self.rect.left
            arrow_y = self.rect.centery
            arrow_x1 = arrow_x + 30 * math.cos(0.9 * math.pi)
            arrow_y1 = arrow_y + 30 * math.sin(0.9 * math.pi)
            arrow_x2 = arrow_x + 30 * math.cos(1.1 * math.pi)
            arrow_y2 = arrow_y + 30 * math.sin(1.1 * math.pi)
            gfxdraw.filled_polygon(
                screen,
                [(arrow_x, arrow_y), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)],
                (0, 0, 0),
            )
            gfxdraw.aapolygon(
                screen,
                [(arrow_x, arrow_y), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)],
                (0, 0, 0),
            )
            pygame.draw.aaline(
                screen, "black", (arrow_x, arrow_y), (arrow_x - 100, arrow_y), 5
            )

    def __eq__(self, other):
        if isinstance(other, Tile):
            return self.id == other.id
        return False


class Edge:
    def __init__(self, fromTile: Tile, toTile: Tile, label=""):
        self.fromTile = fromTile
        self.toTile = toTile
        self.labels: set[str] = {label}

    def addLabel(self, label):
        self.labels.add(label)

    def renameLabel(self, old, new):
        if old in self.labels:
            self.labels.remove(old)
            self.labels.add(new)

    def isEmpty(self):
        return len(self.labels) == 0

    def removeLabel(self, label):
        if label in self.labels:
            self.labels.remove(label)

    def __eq__(self, other):
        if isinstance(other, Edge):
            return self.fromTile == other.fromTile and self.toTile == other.toTile
        return False

    def draw(self, screen):
        arrow_length = 30
        radius = self.fromTile.rect.width // 2
        arrow_angle = math.pi / 6

        displayedStr = ""
        for label in self.labels:
            displayedStr += (label if label != "" else "ε") + ", "
        displayedStr = displayedStr[:-2]

        if self.fromTile == self.toTile:
            offset = self.fromTile.rect.width
            rect = pygame.Rect(
                self.fromTile.rect.centerx,
                self.fromTile.rect.centery - offset,
                offset,
                offset,
            )
            pygame.draw.arc(screen, (255, 0, 0), rect, -0.5 * math.pi, math.pi, 2)
            angle = 0.9 * math.pi
            arrow_x = self.fromTile.rect.centerx + radius
            arrow_y = self.fromTile.rect.centery
            arrow_x1 = arrow_x - arrow_length * math.cos(angle + arrow_angle / 2)
            arrow_y1 = arrow_y - arrow_length * math.sin(angle + arrow_angle / 2)
            arrow_x2 = arrow_x - arrow_length * math.cos(angle - arrow_angle / 2)
            arrow_y2 = arrow_y - arrow_length * math.sin(angle - arrow_angle / 2)
            font = pygame.font.Font(None, 50)
            text = font.render(displayedStr, True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.topright)
            screen.blit(text, text_rect)
            gfxdraw.filled_polygon(
                screen,
                [(arrow_x, arrow_y), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)],
                (255, 0, 0),
            )
            gfxdraw.aapolygon(
                screen,
                [(arrow_x, arrow_y), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)],
                (255, 0, 0),
            )
        else:
            start_x, start_y = self.fromTile.rect.centerx, self.fromTile.rect.centery
            end_x, end_y = self.toTile.rect.centerx, self.toTile.rect.centery
            angle = math.atan2(end_y - start_y, end_x - start_x)
            tailDeviateAngle = math.pi * 0.1
            tailArcHeight = 20
            tail_x, tail_y = start_x + radius * math.cos(
                angle + tailDeviateAngle
            ), start_y + radius * math.sin(angle + tailDeviateAngle)
            head_x, head_y = end_x + radius * math.cos(
                angle - tailDeviateAngle + math.pi
            ), end_y + radius * math.sin(angle - tailDeviateAngle + math.pi)
            distance = math.sqrt((tail_x - head_x) ** 2 + (tail_y - head_y) ** 2)
            mid_x, mid_y = (tail_x + head_x) / 2, (tail_y + head_y) / 2
            angle_offset = math.atan(tailArcHeight * 2 / distance)
            r = distance / (2 * math.sin(2 * angle_offset))
            center_x, center_y = mid_x + (r - tailArcHeight) * math.sin(
                angle
            ), mid_y - (r - tailArcHeight) * math.cos(angle)
            from_angle, to_angle = (
                math.pi * 0.5 + angle - 2 * angle_offset,
                math.pi * 0.5 + angle + 2 * angle_offset,
            )
            arcRect = pygame.Rect(center_x - r, center_y - r, 2 * r, 2 * r)
            pygame.draw.arc(screen, (255, 0, 0), arcRect, -to_angle, -from_angle, 2)
            finalAngle = angle - tailDeviateAngle
            arrow_x1 = head_x - arrow_length * math.cos(finalAngle + arrow_angle / 2)
            arrow_y1 = head_y - arrow_length * math.sin(finalAngle + arrow_angle / 2)
            arrow_x2 = head_x - arrow_length * math.cos(finalAngle - arrow_angle / 2)
            arrow_y2 = head_y - arrow_length * math.sin(finalAngle - arrow_angle / 2)
            gfxdraw.filled_polygon(
                screen,
                [(head_x, head_y), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)],
                (255, 0, 0),
            )
            gfxdraw.aapolygon(
                screen,
                [(head_x, head_y), (arrow_x1, arrow_y1), (arrow_x2, arrow_y2)],
                (255, 0, 0),
            )
            font = pygame.font.Font(None, 50)
            text = font.render(displayedStr, True, (0, 0, 0))
            yOffset = 20 if self.fromTile.id < self.toTile.id else -20
            text_rect = text.get_rect(
                center=((tail_x + head_x) // 2, (tail_y + head_y) // 2 + yOffset)
            )
            screen.blit(text, text_rect)
