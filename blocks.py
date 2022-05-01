# CS403 Final Project: tryPy
# Team Members: Peter Zhang, Madeline Moore, Cara Cannarozzi

import pygame
from constants import *

# class for blocks and block features
class Block:
    # constructor for blocks, sets default values
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

    # draws blocks
    def render(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        font = pygame.freetype.SysFont(*TIMES_FONT)
        #adds text to block
        font.render_to(surface, (self.x + TIMES_FONT[1]//2, self.y + TIMES_FONT[1]//2), self.text, BLACK, size=20)

    # checks if coordinates are inside the block
    def within_bounds(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height

    # moves block by specified x and y
    def move(self, x, y):
        self.x += x
        self.y += y
        self.rect = (self.x, self.y, self.width, self.height)
        if self.next is not None:
            self.next.move(x, y)

    # checks if block has text box
    def has_textbox(self):
        return self.has_tb

    # returns center coordinates of block
    def get_center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)

    # returns left coordinates of block (leftmost x value, center y value)
    def get_left(self):
        return (self.x, self.y + self.height // 2)

    # returns oldest parent (highest in stack of connected blocks)
    def greatest_parent(self):
        cur = self
        while (cur.parent is not None):
            cur = cur.parent
        return cur

    # snaps blocks together
    def snap(self, other_block):
        self.parent = other_block
        other_block.next = self
        # if snapping to an if, else, while, or for block, indent the snap
        self.x = other_block.x + (other_block.width // (TIMES_FONT[1]//2)) if isinstance(other_block, (If, Else, While, For)) else other_block.x
        self.y = other_block.y + other_block.height
        self.rect = (self.x, self.y, self.width, self.height)

    # snaps blocks together, unindenting (to add code after if, else, while, or for loop that's not in the condition/loop body)
    def unindent_snap(self, other_block):
        self.parent = other_block
        other_block.next = self
        self.x = other_block.x - (other_block.width // (TIMES_FONT[1]//2))
        self.y = other_block.y + other_block.height
        self.rect = (self.x, self.y, self.width, self.height)

    # unsnaps blocks
    def unsnap(self):
        if self.parent is not None:
            self.parent.next = None
        self.parent = None

    # turns blocks into tokens
    def tokenize(self):
        # handles setting variables
        if isinstance(self, Var):
            return [self.tb.text, '=', self.tb2.text]
        # handles printing
        if isinstance(self, Print):
            return ['print', '(', self.tb.text, ')']
        # handles blocks that have text boxes
        elif isinstance(self, BlockWithTextBox):
            return [self.text, self.tb.text, ':']
        # handles breaks (and other blocks without text)
        else:
            return [self.text]

# class for text boxes and text box features
class TextBox(Block):
    # constructor for text boxes, sets default values
    def __init__(self, x, y, width, height, active_color):
        super().__init__(x, y, width, height, WHITE, '')
        self.is_active = False
        self.activeColor = active_color

    # activates text box (allows user to start typing)
    def activate(self):
        self.color = self.activeColor
        self.is_active = True

    # deactivates text box (when user is done typing)
    def deactivate(self):
        self.color = WHITE
        self.is_active = False

    # deletes one character from text
    def backspace(self):
        self.text = self.text[:-1]

    # adds one character to text
    def update_text(self, char):
        self.text += char

    # resets text box dimensions
    def reset_x_y(self, x, y):
        self.x = x
        self.y = y
        self.rect = (self.x, self.y, self.width, self.height)

# class for blocks with text boxes and features for blocks with text boxes
class BlockWithTextBox(Block):
    # constructor for blocks with text boxes, sets default values
    def __init__(self, x, y, width, height, color, text, active_color):
        super().__init__(x, y, width, height, color, text)
        self.tb = TextBox(self.get_tb_x(), self.get_tb_y(), self.get_tb_width(), self.get_tb_height(), active_color)
        self.has_tb = True

    # draws block with text box
    def render(self, surface):
        super().render(surface)
        self.tb.reset_x_y(self.get_tb_x(), self.get_tb_y())
        self.tb.render(surface)

    # moves block by specified x and y
    def move(self, x, y):
        super().move(x, y)
        self.tb.move(x, y)

    # checks if coordinate are within text box bounds
    def within_textbox_bounds(self, x, y):
        if self.tb.within_bounds(x, y):
            # activates text box
            self.tb.activate()
            return True
        return False

    # deletes one character from text box
    def backspace(self):
        self.tb.backspace()

    # adds one character to text box
    def update_text(self, char):
        self.tb.update_text(char)

    # deactivates text box (user is done typing)
    def deactivate_textbox(self):
        self.tb.deactivate()

    # returns left x value of text box
    def get_tb_x(self):
        return self.x + TIMES_FONT[1]//2

    # returns bottom y value of text box
    def get_tb_y(self):
        return self.y + TIMES_FONT[1]*3

    # returns width of text box
    def get_tb_width(self):
        return self.width - TIMES_FONT[1]

    # returns height of text box
    def get_tb_height(self):
        return self.height // 3

# class for start block (initializes and sets default values)
class Start(Block):
    def __init__(self, x, y, width, height):
        # super() of Start is Block since there are no text boxes
        super().__init__(x, y, width, height, GREEN, 'start')

# class for if block (initializes and sets default values)
class If(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        # super() of If is BlockWithTextBox since there is one text box
        super().__init__(x, y, width, height, PURPLE, 'if', LIGHTPURPLE)

# class for else block (initializes and sets default values)
class Else(Block):
    def __init__(self, x, y, width, height):
        # super() of Else is Block since there are no text boxes
        super().__init__(x, y, width, height, LIGHTPURPLE, 'else')

# class for while block (initializes and sets default values)
class While(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        # super() of While is BlockWithTextBox since there is one text box
        super().__init__(x, y, width, height, BLUE, 'while', LIGHTBLUE)

# class for for block (initializes and sets default values)
class For(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        # super() of For is BlockWithTextBox since there is one text box
        super().__init__(x, y, width, height, YELLOW, 'for', LIGHTYELLOW)

# class for break block (initializes and sets default values)
class Break(Block):
    def __init__(self, x, y, width, height):
        # super() of Break is Block since there are no text boxes
        super().__init__(x, y, width, height, RED, 'break')

# class for print block (initializes and sets default values)
class Print(BlockWithTextBox):
    def __init__(self, x, y, width, height):
        # super() of Print is BlockWithTextBox since there are is one text box
        super().__init__(x, y, width, height, ORANGE, 'print', LIGHTORANGE)

# class for variable assignment block
class Var(BlockWithTextBox):
    # constructor, sets default values (inherits from BlockWithTextBox but is different since there are two text boxes)
    def __init__(self, x, y, width, height):
        activecolor = LIGHTBROWN
        super().__init__(x, y, width, height, BROWN, '', activecolor) 
        # two text boxes
        self.tb = TextBox(self.get_tb_x(), self.get_tb_y(), self.get_tb_width(), self.get_tb_height(), activecolor)
        self.tb2 = TextBox(self.get_tb2_x(), self.get_tb_y(), self.get_tb_width(), self.get_tb_height(), activecolor)

    # draws block with two text boxes
    def render(self, surface):
        super().render(surface)
        self.tb2.reset_x_y(self.get_tb2_x(), self.get_tb_y())
        self.tb2.render(surface)
        font = pygame.freetype.SysFont(*TIMES_FONT)
        #adds "=" between text boxes
        font.render_to(surface, ((self.x + self.width//2 - TIMES_FONT[1]//2), (self.y + self.height//2 - 2)), "=", BLACK, size=20)

    # moves block by specified x and y
    def move(self, x, y):
        super().move(x, y)
        self.tb2.move(x, y)

    # checks if coordinates are within text box bounds
    def within_textbox_bounds(self, x, y):
        # checks within bounds of LHS text box
        if self.tb.within_bounds(x, y):
            self.tb.activate()
            return True
        # checks within bounds of RHS text box
        elif self.tb2.within_bounds(x, y):
            self.tb2.activate()
            return True
        return False

    # deletes one character from active text box
    def backspace(self):
        # if in LHS text box
        if self.tb.is_active: self.tb.backspace()
        # if in RHS text box
        elif self.tb2.is_active: self.tb2.backspace()

    # adds one character to active text box
    def update_text(self, char):
        # if in LHS text box
        if self.tb.is_active: self.tb.update_text(char)
        # if in RHS text box
        elif self.tb2.is_active: self.tb2.update_text(char)

    # deactivates text box (user is done typing)
    def deactivate_textbox(self):
        # if in LHS text box
        if self.tb.is_active: self.tb.deactivate()
        # if in RHS text box
        elif self.tb2.is_active: self.tb2.deactivate()
    
    # returns left x value of LHS text box
    def get_tb_x(self):
        return self.x + TIMES_FONT[1]//2

    # returns bottom y value of text box
    def get_tb_y(self):
        return self.y + TIMES_FONT[1]

    # returns left x value of RHS text box
    def get_tb2_x(self):
        return self.x + self.width - self.tb.width - TIMES_FONT[1]//2 

    # returns width of text box
    def get_tb_width(self):
        return self.width // 2 - (TIMES_FONT[1]//2)*3

    # returns height of text box
    def get_tb_height(self):
        return self.height - TIMES_FONT[1]*2