from multiprocessing import Condition
import pygame
from constants import *

class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = WHITE
        self.rect = (x, y, width, height)
        self.text = 'base'
        self.has_cond = False
        self.parent = None
        self.next = None

    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.freetype.SysFont(*TIMES_FONT)
        font.render_to(surface, (self.x, self.y), self.text, BLACK, size=self.width // 4)

    def within_bounds(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def move(self, x, y):
        self.x += x
        self.y += y
        self.rect = (self.x, self.y, self.width, self.height)
        if self.next is not None:
            self.next.move(x, y)

    def has_condition(self):
        return self.has_cond

    def get_center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)

    def snap(self, other_block):
        self.parent = other_block
        other_block.next = self
        self.x = other_block.x + (other_block.width // 5) if isinstance(other_block, BlockWithCond) else other_block.x
        self.y = other_block.y + other_block.height
        self.rect = (self.x, self.y, self.width, self.height)

    def unsnap(self):
        if self.parent is not None:
            self.parent.next = None
        self.parent = None


class BlockWithCond(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.has_cond = True
        self.c_width = width - 10
        self.c_height = height // 3
        # if you change the next 2 lines make sure to change this also in the snap function
        self.c_x = x + 5
        self.c_y = y + 25 #change from hardcoded to adaptive to font size
        self.c_color = WHITE
        self.c_rect = (self.c_x, self.c_y, self.c_width, self.c_height)
        self.c_text = ''
        self.activeCond = False
        self.activeColor = WHITE

    def render(self, surface):
        super().render(surface)
        pygame.draw.rect(surface, self.c_color, self.c_rect)
        font = pygame.freetype.SysFont(*TIMES_FONT)
        font.render_to(surface, (self.c_x, self.c_y), self.c_text, BLACK, size=self.c_width // 4)

    def move(self, x, y):
        super().move(x, y)
        self.c_x += x
        self.c_y += y
        self.c_rect = (self.c_x, self.c_y, self.c_width, self.c_height)

    def within_textBox_bounds(self, x, y):
        if self.c_x <= x <= self.c_x + self.c_width and self.c_y <= y <= self.c_y + self.c_height:
            self.activeCond = True
            self.c_color = self.activeColor
            return True
        #self.c_color = WHITE
        return False

    def backspace(self):
        self.c_text = self.c_text[:-1]

    def update_text(self, char):
        self.c_text += char

    def get_pos(self):
        # this is top left of block
        return self.x, self.y

    def snap(self, other_block):
        super().snap(other_block)
        # update textbox
        self.c_x = self.x + 5
        self.c_y = self.y + 25
        self.c_rect = (self.c_x, self.c_y, self.c_width, self.c_height)
class Start(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = GREEN
        self.text = 'start'

class If(BlockWithCond):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = PURPLE
        self.activeColor = LIGHTPURPLE
        self.text = 'if'

class While(BlockWithCond):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = BLUE
        self.activeColor = LIGHTBLUE
        self.text = 'while'
class For(BlockWithCond):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = YELLOW
        self.activeColor = LIGHTYELLOW
        self.text = 'for'

class Break(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = RED
        self.text = 'break'

class Print(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = ORANGE
        self.text = 'print'
