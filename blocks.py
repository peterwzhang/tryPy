from multiprocessing import Condition
import pygame
from constants import *

class Block:
    def __init__(self, x, y, width, height, color=WHITE, text='base'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = (x, y, width, height)
        self.text = text
        self.has_tb = False
        self.parent = None
        self.next = None

    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.freetype.SysFont(*TIMES_FONT)
        font.render_to(surface, (self.x + TIMES_FONT[1]//2, self.y + TIMES_FONT[1]//2), self.text, BLACK, size=20)

    def within_bounds(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    def move(self, x, y):
        self.x += x
        self.y += y
        self.rect = (self.x, self.y, self.width, self.height)
        if self.next is not None:
            self.next.move(x, y)

    def has_textbox(self):
        return self.has_tb

    def get_center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)

    def greatest_parent(self):
        cur = self
        while (cur.parent is not None):
            cur = cur.parent
        return cur

    def snap(self, other_block):
        self.parent = other_block
        other_block.next = self
        self.x = other_block.x + (other_block.width // (TIMES_FONT[1]//2)) if isinstance(other_block, BlockWithTextBox) else other_block.x
        self.y = other_block.y + other_block.height
        self.rect = (self.x, self.y, self.width, self.height)

    def unsnap(self):
        if self.parent is not None:
            self.parent.next = None
        self.parent = None


class TextBox(Block):
    def __init__(self, x, y, width, height, active_color):
        super().__init__(x, y, width, height, WHITE, '')
        self.is_active = False
        self.activeColor = active_color

    def activate(self):
        self.color = self.activeColor
        self.is_active = True

    def deactivate(self):
        self.color = WHITE
        self.is_active = False

    def backspace(self):
        self.text = self.text[:-1]

    def update_text(self, char):
        self.text += char


class BlockWithTextBox(Block):
    def __init__(self, x, y, width, height, color, text, active_color):
        super().__init__(x, y, width, height, color, text)
        # if you change the next 2 lines make sure to change this also in the snap function
        self.tb_x = x + TIMES_FONT[1]//2
        self.tb_y = y + TIMES_FONT[1]*3
        self.tb_width = width - TIMES_FONT[1]
        self.tb_height = height // 3
        self.tb = TextBox(self.tb_x, self.tb_y, self.tb_width, self.tb_height, active_color)
        self.has_tb = True

    def render(self, surface):
        super().render(surface)
        self.tb.render(surface)

    def move(self, x, y):
        super().move(x, y)
        self.tb.move(x, y)

    def within_textbox_bounds(self, x, y):
        if self.tb.within_bounds(x, y):
            self.tb.activate()
            return True
        return False

    def backspace(self):
        self.tb.backspace()

    def update_text(self, char):
        self.tb.update_text(char)

    def snap(self, other_block):
        temp_x = self.x
        temp_y = self.y
        super().snap(other_block)
        self.tb.x = self.tb.x + abs(self.x - temp_x)
        self.tb.y = self.tb.y + abs(self.y - temp_y)
        self.tb.rect = (self.tb.x, self.tb.y, self.tb.width, self.tb.height)

    def deactivate_textbox(self):
        self.tb.deactivate()


class Start(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, GREEN, 'start')

class If(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, PURPLE, 'if', LIGHTPURPLE)

class Else(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, LIGHTPURPLE, 'else', LIGHTERPURPLE)

class While(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, BLUE, 'while', LIGHTBLUE)

class For(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, YELLOW, 'for', LIGHTYELLOW)

class Break(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, RED, 'break')

class Print(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, ORANGE, 'print', LIGHTORANGE)

class Var(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        activecolor = LIGHTBROWN
        super().__init__(x, y, width, height, BROWN, '', activecolor)
        self.tb_x = x + TIMES_FONT[1]//2
        self.tb_y = y + TIMES_FONT[1]
        self.tb_width = width // 2 - (TIMES_FONT[1]//2)*3
        self.tb_height = height - TIMES_FONT[1]*2
        self.tb = TextBox(self.tb_x, self.tb_y, self.tb_width, self.tb_height, activecolor)
        self.tb2 = TextBox(x + width - self.tb_width - 5, self.tb_y, self.tb_width, self.tb_height, activecolor)

    def render(self, surface):
        super().render(surface)
        self.tb2.render(surface)
        font = pygame.freetype.SysFont(*TIMES_FONT)
        font.render_to(surface, ((self.x + self.width//2 - TIMES_FONT[1]//2), (self.y + self.height//2 - 2)), "=", BLACK, size=20)

    def move(self, x, y):
        super().move(x, y)
        self.tb2.move(x, y)

    def within_textbox_bounds(self, x, y):
        if self.tb.within_bounds(x, y):
            self.tb.activate()
            return True
        elif self.tb2.within_bounds(x, y):
            self.tb2.activate()
            return True
        return False

    def backspace(self):
        if self.tb.is_active: self.tb.backspace()
        elif self.tb2.is_active: self.tb2.backspace()

    def update_text(self, char):
        if self.tb.is_active: self.tb.update_text(char)
        elif self.tb2.is_active: self.tb2.update_text(char)

    def snap(self, other_block):
        temp_x = self.x
        temp_y = self.y
        super().snap(other_block)
        self.tb2.x = self.tb2.x + abs(self.x - temp_x)
        self.tb2.y = self.tb2.y + abs(self.y - temp_y)
        self.tb2.rect = (self.tb2.x, self.tb2.y, self.tb2.width, self.tb2.height)

    def deactivate_textbox(self):
        if self.tb.is_active: self.tb.deactivate()
        elif self.tb2.is_active: self.tb2.deactivate()