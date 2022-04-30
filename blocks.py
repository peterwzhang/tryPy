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

    def get_left(self):
        return (self.x, self.y + self.height // 2)

    def greatest_parent(self):
        cur = self
        while (cur.parent is not None):
            cur = cur.parent
        return cur

    def snap(self, other_block):
        self.parent = other_block
        other_block.next = self
        self.x = other_block.x + (other_block.width // (TIMES_FONT[1]//2)) if isinstance(other_block, (If, Else, While, For)) else other_block.x
        self.y = other_block.y + other_block.height
        self.rect = (self.x, self.y, self.width, self.height)

    def unindent_snap(self, other_block):
        self.parent = other_block
        other_block.next = self
        self.x = other_block.x - (other_block.width // (TIMES_FONT[1]//2))
        self.y = other_block.y + other_block.height
        self.rect = (self.x, self.y, self.width, self.height)

    def unsnap(self):
        if self.parent is not None:
            self.parent.next = None
        self.parent = None

    def tokenize(self):
        if isinstance(self, Var):
            return [self.tb.text, '=', self.tb2.text]
        if isinstance(self, Print):
            return ['print', '(', self.tb.text, ')']
        elif isinstance(self, BlockWithTextBox):
            return [self.text, self.tb.text, ':']
        else:
            return [self.text]


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

    def reset_x_y(self, x, y):
        self.x = x
        self.y = y
        self.rect = (self.x, self.y, self.width, self.height)


class BlockWithTextBox(Block):
    def __init__(self, x, y, width, height, color, text, active_color):
        super().__init__(x, y, width, height, color, text)
        self.tb = TextBox(self.get_tb_x(), self.get_tb_y(), self.get_tb_width(), self.get_tb_height(), active_color)
        self.has_tb = True

    def render(self, surface):
        super().render(surface)
        self.tb.reset_x_y(self.get_tb_x(), self.get_tb_y())
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

    def deactivate_textbox(self):
        self.tb.deactivate()

    def get_tb_x(self): return self.x + TIMES_FONT[1]//2

    def get_tb_y(self): return self.y + TIMES_FONT[1]*3

    def get_tb_width(self): return self.width - TIMES_FONT[1]

    def get_tb_height(self): return self.height // 3




class Start(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, GREEN, 'start')

class If(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, PURPLE, 'if', LIGHTPURPLE)

class Else(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, LIGHTPURPLE, 'else')

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
        self.tb = TextBox(self.get_tb_x(), self.get_tb_y(), self.get_tb_width(), self.get_tb_height(), activecolor)
        self.tb2 = TextBox(self.get_tb2_x(), self.get_tb_y(), self.get_tb_width(), self.get_tb_height(), activecolor)

    def render(self, surface):
        super().render(surface)
        self.tb2.reset_x_y(self.get_tb2_x(), self.get_tb_y())
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

    def deactivate_textbox(self):
        if self.tb.is_active: self.tb.deactivate()
        elif self.tb2.is_active: self.tb2.deactivate()
    
    def get_tb_x(self): return self.x + TIMES_FONT[1]//2

    def get_tb_y(self): return self.y + TIMES_FONT[1]

    def get_tb2_x(self): return self.x + self.width - self.tb.width - TIMES_FONT[1]//2 

    def get_tb_width(self): return self.width // 2 - (TIMES_FONT[1]//2)*3

    def get_tb_height(self): return self.height - TIMES_FONT[1]*2
