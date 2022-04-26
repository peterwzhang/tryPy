import pygame
from constants import *

class Block:

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = RED
        self.rect = (x, y, width, height)
        self.text = "base"

    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.freetype.SysFont(*TIMES_FONT)
        font.render_to(surface, (self.x, self.y), self.text, BLACK, size=self.width / 4)

    def within_bounds(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def move(self, x, y):
        self.x += x
        self.y += y
        self.rect = (self.x, self.y, self.width, self.height)


class Conditional(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = GREEN
        self.text = "cond"

class Loop(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = BLUE
        self.text = "loop"

class Start(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = YELLOW
        self.text = "start"