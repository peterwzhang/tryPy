# CS403 Final Project: tryPy
# Team Members: Peter Zhang, Madeline Moore, Cara Cannarozzi

from math import ceil
import pygame
import pygame.freetype
from blocks import *
from constants import *

# returns the mouse position
def get_mouse_pos():
    return pygame.mouse.get_pos()

# class for rendering and managing blocks
class BlockManager:
    # constructor for blocks
    def __init__(self, screen):
        self.blocks = []
        self.main_blocks = []
        self.screen = screen

    # adds a block to block list
    def add_block(self, block):
        self.blocks.append(block)

    # removes block from block list
    def delete_block(self, block):
        self.blocks.remove(block)

    # adds blocks to main blocks list
    def add_main_block(self, block):
        self.main_blocks.append(block)
        next = block.next
        while (next is not None):
            self.main_blocks.append(next)
            next = next.next

    # removes blocks from main blocks list
    def remove_main_block(self, block):
        self.main_blocks.remove(block)
        next = block.next
        while (next is not None):
            self.main_blocks.remove(next)
            next = next.next

    # draws blocks on screen
    def render_blocks(self):
        self.screen.fill(BLACK)
        for block in self.blocks:
            block.render(self.screen)
        pygame.display.update() # can optimize this to only update things that need to be updated

    # this returns a list incase we want to make some sort of priority system later
    # checks if blocks are touching
    def check_block_collisions(self, x, y):
        # handle if multiple blocks on top of each other
        collisions = []
        for block in self.blocks:
            if block.within_bounds(x, y):
                collisions.append(block)
        return collisions if len(collisions) > 0 else [None]

    # checks if in a text box
    def check_textbox_collisions(self, selectedBlock, x, y):
        if selectedBlock.within_textbox_bounds(x, y):   
            return True
        return False

    # this returns a list incase we want to make some sort of priority system later
    # returns list of valid snaps (at center or left)
    def get_snap_collisions(self, selectedBlock):
        if selectedBlock is None:
            return []
        snap_collisions = []
        for block in self.blocks:
            # checks if center block collision for snap
            if block.within_bounds(*selectedBlock.get_center()) and block != selectedBlock:
                snap_collisions.append(block)
            # checks if left block collision for snap
            if block.within_bounds(*selectedBlock.get_left()) and block != selectedBlock:
                snap_collisions.append(block)
        return snap_collisions if len(snap_collisions) > 0 else [None]

    # checks if collision is a valid snap
    def check_for_snap(self, selectedBlock):
        if selectedBlock is None:
            return
        snap_candidates = self.get_snap_collisions(selectedBlock)
        # if there is a valid snap collision, snap into correct place
        if snap_candidates[0] is not None:
            # if snap is at left of block, unindent
            if selectedBlock.within_bounds(*snap_candidates[0].get_left()):
                selectedBlock.unindent_snap(snap_candidates[0])
            # if snap is at center, snap into correct spot (inline or indented)
            else:
                selectedBlock.snap(snap_candidates[0])
            if not isinstance(selectedBlock, Start) and isinstance(selectedBlock.greatest_parent(), Start):
                self.main_blocks.append(selectedBlock)
        else:
            # unsnaps blocks
            if not isinstance(selectedBlock, Start) and isinstance(selectedBlock.greatest_parent(), Start):
                self.main_blocks.remove(selectedBlock)
            selectedBlock.unsnap()

    # resets blocks to starting position
    def reset(self):
        self.blocks = []
        self.main_blocks = []
        init_blocks(self)

    # returns python code generated by tryPy
    def get_python_code(self):
        code = ''
        for block in self.main_blocks:
            num_indents = abs(ceil((self.blocks[0].x - block.x) / (BLOCK_WIDTH // (TIMES_FONT[1]//2))))
            code += ('\t' * num_indents) + ' '.join(block.tokenize()) + '\n'
        return code

    # executes python code generated by tryPy
    def run_blocks(self):
        # compiles code returned by get_python_code
        code_obj = compile(self.get_python_code(), 'blocks', 'exec')
        print('CODE OUTPUT:')
        exec(code_obj)

# starts pygame, sets up screen display and logo
def setup_screen(title, x, y):
    pygame.init()   # initialize the pygame module
    pygame.display.set_caption(title)
    screen = pygame.display.set_mode((x,y))
    logo = pygame.image.load('./manual/pictures/logo.png')
    pygame.display.set_icon(logo)
    return screen

# initialized blocks in the menu (stacked on left sided of the screen)
# Adds one Start block and 6 instances of every other block
def init_blocks(manager):
    manager.add_block(Start(0, 0, BLOCK_WIDTH, 50))
    for i in range(6):
        manager.add_block(If(0, 50, BLOCK_WIDTH, 75))
        manager.add_block(Else(0, 125, BLOCK_WIDTH, 50))
        manager.add_block(While(0, 175, BLOCK_WIDTH, 75))
        manager.add_block(For(0, 250, BLOCK_WIDTH, 75))
        manager.add_block(Print(0, 325, BLOCK_WIDTH, 75))
        manager.add_block(Var(0, 400, BLOCK_WIDTH, 50))
        manager.add_block(Break(0, 450, BLOCK_WIDTH, 50))

# main execution function
def main():
    # sets up screen and blocks
    screen = setup_screen(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
    tryPy_manager = BlockManager(screen)
    tryPy_manager.reset()

    # variables for running, dragging, text boxes
    running = True
    selectedBlock = None
    dragging = False
    isActiveTextBox = False

    # runs tryPy until quit
    while running:
        # executes events
        for event in pygame.event.get():
            # quits tryPy
            if event.type == pygame.QUIT:
                running = False
            # handles mouse clicks (dragging blocks)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                # deactivates text box of previous selected block 
                if selectedBlock and selectedBlock.has_textbox():
                    selectedBlock.deactivate_textbox()
                # checks for block collisions, sets new selected block 
                selectedBlock = tryPy_manager.check_block_collisions(*event.pos)[0]
                # if new selected block has text box, check if clicked within text box
                if selectedBlock and selectedBlock.has_textbox():
                    isActiveTextBox = tryPy_manager.check_textbox_collisions(selectedBlock, *event.pos)
                else:
                    isActiveTextBox = False
            # handles mouse releases
            elif event.type == pygame.MOUSEBUTTONUP:
                # checks if there is a valid snap
                tryPy_manager.check_for_snap(selectedBlock)
                dragging = False
            # handles moving the mouse
            elif event.type == pygame.MOUSEMOTION:
                # if a block is selected, move it with the mouse
                if selectedBlock and dragging:
                    selectedBlock.move(*event.rel)
            # handles keyboard typing
            elif event.type == pygame.KEYDOWN:
                # if a textbox is active, type keys in textbox
                if isActiveTextBox:
                    # if backspace is pushed, delete
                    if event.key == pygame.K_BACKSPACE:
                        selectedBlock.backspace()
                    # else, updates text with character of key pressed
                    else:
                        selectedBlock.update_text(event.unicode)
                # when "s" is pressed not in text box, run code
                elif event.key == pygame.K_s:
                    tryPy_manager.run_blocks()
                # when "r" is pressed not in text box, reset blocks
                elif event.key == pygame.K_r:
                    tryPy_manager.reset()
                # when "p" is pressed not in text box, print python code generated by tryPy blocks
                elif event.key == pygame.K_p:
                    print(tryPy_manager.get_python_code())
            #updates blocks
            tryPy_manager.render_blocks()

if __name__=="__main__":
    main()