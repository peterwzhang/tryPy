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
        font.render_to(surface, (self.x + 5, self.y + 5), self.text, BLACK, size=20)

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
        self.x = other_block.x + (other_block.width // 5) if isinstance(other_block, BlockWithTextBox) else other_block.x
        self.y = other_block.y + other_block.height
        self.rect = (self.x, self.y, self.width, self.height)

    def unsnap(self):
        if self.parent is not None:
            self.parent.next = None
        self.parent = None


class BlockWithTextBox(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.has_cond = True
        self.tb_width = width - 10
        self.tb_height = height // 3
        # if you change the next 2 lines make sure to change this also in the snap function
        self.tb_x = x + 5
        self.tb_y = y + 30 #change from hardcoded to adaptive to font size
        self.tb_color = WHITE
        self.tb_rect = (self.tb_x, self.tb_y, self.tb_width, self.tb_height)
        self.tb_text = ''
        self.activeCond = False
        self.activeColor = WHITE

    def render(self, surface):
        super().render(surface)
        pygame.draw.rect(surface, self.tb_color, self.tb_rect)
        font = pygame.freetype.SysFont(*TIMES_FONT)
        font.render_to(surface, (self.tb_x + 5, self.tb_y + 5), self.tb_text, BLACK, size=20)

    def move(self, x, y):
        super().move(x, y)
        self.tb_x += x
        self.tb_y += y
        self.tb_rect = (self.tb_x, self.tb_y, self.tb_width, self.tb_height)

    def within_textBox_bounds(self, x, y):
        if self.tb_x <= x <= self.tb_x + self.tb_width and self.tb_y <= y <= self.tb_y + self.tb_height:
            self.activeCond = True
            self.tb_color = self.activeColor
            return True
        return False

    def backspace(self):
        self.tb_text = self.tb_text[:-1]

    def update_text(self, char):
        self.tb_text += char

    def snap(self, other_block):
        super().snap(other_block)
        # update textbox
        self.tb_x = self.x + 5
        self.tb_y = self.y + 30
        self.tb_rect = (self.tb_x, self.tb_y, self.tb_width, self.tb_height)

    def disactivate_textBox(self):
        self.tb_color = WHITE

class BlockSetVar(Block): 
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.text = ''
        self.has_cond = True
        self.var_tb_width = width // 2 - 15
        self.var_tb_height = height - 20
        self.val_tb_width = self.var_tb_width
        self.val_tb_height = self.var_tb_height
        # if you change the next 2 lines make sure to change this also in the snap function
        self.var_tb_x = x + 5
        self.var_tb_y = y + 10 #change from hardcoded to adaptive to font size
        self.val_tb_x = self.x + self.width - 5 - self.val_tb_width
        self.val_tb_y = self.var_tb_y
        self.var_tb_color = WHITE
        self.val_tb_color = WHITE
        self.var_tb_rect = (self.var_tb_x, self.var_tb_y, self.var_tb_width, self.var_tb_height)
        self.val_tb_rect = (self.val_tb_x, self.val_tb_y, self.val_tb_width, self.val_tb_height)
        self.var_tb_text = ''
        self.val_tb_text = ''
        self.var_activeCond = False
        self.val_activeCond = False
        self.activeColor = WHITE

    def render(self, surface):
        super().render(surface)
        pygame.draw.rect(surface, self.var_tb_color, self.var_tb_rect)
        pygame.draw.rect(surface, self.val_tb_color, self.val_tb_rect)
        font = pygame.freetype.SysFont(*TIMES_FONT)
        font.render_to(surface, (self.var_tb_x + 5, self.var_tb_y + 5), self.var_tb_text, BLACK, size=20)
        font.render_to(surface, (self.val_tb_x + 5, self.val_tb_y + 5), self.val_tb_text, BLACK, size=20)
        font.render_to(surface, ((self.x + self.width//2 - 5), (self.y + self.height//2 - 2)), "=", BLACK, size=20)

    def move(self, x, y):
        super().move(x, y)
        self.var_tb_x += x
        self.var_tb_y += y
        self.var_tb_rect = (self.var_tb_x, self.var_tb_y, self.var_tb_width, self.var_tb_height)
        self.val_tb_x += x
        self.val_tb_y += y
        self.val_tb_rect = (self.val_tb_x, self.val_tb_y, self.val_tb_width, self.val_tb_height)

    def within_textBox_bounds(self, x, y):
        if self.var_tb_x <= x <= self.var_tb_x + self.var_tb_width and self.var_tb_y <= y <= self.var_tb_y + self.var_tb_height:
            self.var_activeCond = True
            self.var_tb_color = self.activeColor
            return True
        if self.val_tb_x <= x <= self.val_tb_x + self.val_tb_width and self.val_tb_y <= y <= self.val_tb_y + self.val_tb_height:
            self.val_activeCond = True
            self.val_tb_color = self.activeColor
            return True
        return False

    def backspace(self):
        if self.var_activeCond: self.var_tb_text = self.var_tb_text[:-1]
        elif self.val_activeCond: self.val_tb_text = self.val_tb_text[:-1]

    def update_text(self, char):
        if self.var_activeCond: self.var_tb_text += char
        elif self.val_activeCond: self.val_tb_text += char

    def snap(self, other_block):
        super().snap(other_block)
        # update textbox
        self.var_tb_x = self.x + 5
        self.var_tb_y = self.y + 10
        self.val_tb_x =  self.x + self.width - 5 - self.val_tb_width
        self.val_tb_y = self.var_tb_y
        self.val_tb_rect = (self.val_tb_x, self.val_tb_y, self.val_tb_width, self.val_tb_height)
        self.var_tb_rect = (self.var_tb_x, self.var_tb_y, self.var_tb_width, self.var_tb_height)

    def disactivate_textBox(self):
        if self.var_activeCond: 
            self.var_activeCond = False
            self.var_tb_color = WHITE
        elif self.val_activeCond: 
            self.val_tb_activecond = False
            self.val_tb_color = WHITE

class Start(Block):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = GREEN
        self.text = 'start'

class If(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = PURPLE
        self.activeColor = LIGHTPURPLE
        self.text = 'if'

class Else(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = LIGHTPURPLE
        self.activeColor = LIGHTERPURPLE
        self.text = "else"

class While(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = BLUE
        self.activeColor = LIGHTBLUE
        self.text = 'while'

class For(BlockWithTextBox):
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

class Print(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = ORANGE
        self.activeColor = LIGHTORANGE
        self.text = 'print'

class Var(BlockSetVar):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.color = BROWN
        self.activeColor = LIGHTBROWN

