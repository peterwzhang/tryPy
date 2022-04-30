# import the pygame module, so you can use it
from math import ceil
import pygame
import pygame.freetype
import copy
from blocks import *
from constants import *


def get_mouse_pos():
    return pygame.mouse.get_pos()

class BlockManager:
    def __init__(self, screen):
        self.blocks = []
        self.main_blocks = []
        self.screen = screen

    def add_block(self, block):
        self.blocks.append(block)

    def delete_block(self, block):
        self.blocks.remove(block)

    def add_main_block(self, block):
        self.main_blocks.append(block)
        next = block.next
        while (next is not None):
            self.main_blocks.append(next)
            next = next.next

    def remove_main_block(self, block):
        self.main_blocks.remove(block)
        next = block.next
        while (next is not None):
            self.main_blocks.remove(next)
            next = next.next

    def render_blocks(self):
        self.screen.fill(BLACK)
        for block in self.blocks:
            # should some blocks be rendered before others?
            block.render(self.screen)
        pygame.display.update() # can optimize this to only update things that need to be updated

    # this returns a list incase we want to make some sort of priority system later
    def check_block_collisions(self, x, y):
        # handle if multiple blocks on top of each other
        collisions = []
        for block in self.blocks:
            if block.within_bounds(x, y):
                collisions.append(block)
        return collisions if len(collisions) > 0 else [None]

    def check_textbox_collisions(self, selectedBlock, x, y):
        if selectedBlock.within_textbox_bounds(x, y):
            return True
        return False

    # this returns a list incase we want to make some sort of priority system later
    def get_snap_collisions(self, selectedBlock):
        if selectedBlock is None:
            return []
        snap_collisions = []
        for block in self.blocks:
            if block.within_bounds(*selectedBlock.get_center()) and block != selectedBlock:
                snap_collisions.append(block)
            if block.within_bounds(*selectedBlock.get_left()) and block != selectedBlock:
                snap_collisions.append(block)
        return snap_collisions if len(snap_collisions) > 0 else [None]

    def check_for_snap(self, selectedBlock):
        if selectedBlock is None:
            return
        snap_candidates = self.get_snap_collisions(selectedBlock)
        if snap_candidates[0] is not None:
            if selectedBlock.within_bounds(*snap_candidates[0].get_left()):
                selectedBlock.unindent_snap(snap_candidates[0])
            else:
                selectedBlock.snap(snap_candidates[0])
            if not isinstance(selectedBlock, Start) and isinstance(selectedBlock.greatest_parent(), Start):
                self.main_blocks.append(selectedBlock)
        else:
            if not isinstance(selectedBlock, Start) and isinstance(selectedBlock.greatest_parent(), Start):
                self.main_blocks.remove(selectedBlock)
            selectedBlock.unsnap()

    def reset(self):
        self.blocks = []
        self.main_blocks = []
        init_blocks(self)

    def run_blocks(self):
        code = ''
        for block in self.main_blocks:
            num_indents = abs(ceil((self.blocks[0].x - block.x) / (BLOCK_WIDTH // (TIMES_FONT[1]//2))))
            code += ('\t' * num_indents) + ' '.join(block.tokenize()) + '\n'
        code_obj = compile(code, 'blocks', 'exec')
        print('CODE OUTPUT:')
        exec(code_obj)


def setup_screen(title, x, y):
    pygame.init()   # initialize the pygame module
    pygame.display.set_caption(title)
    screen = pygame.display.set_mode((x,y))
    return screen

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

# define a main function
def main():
    # clock = pygame.time.Clock() # for showing fps
    screen = setup_screen(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
    tryPy_manager = BlockManager(screen)
    tryPy_manager.reset()

    # variable for main game loop + mouse drag handling
    running = True
    selectedBlock = None
    dragging = False
    isActiveTextBox = False

    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                if selectedBlock and selectedBlock.has_textbox():
                    selectedBlock.deactivate_textbox()
                selectedBlock = tryPy_manager.check_block_collisions(*event.pos)[0]
                if selectedBlock and selectedBlock.has_textbox():
                    isActiveTextBox = tryPy_manager.check_textbox_collisions(selectedBlock, *event.pos)
                else:
                    isActiveTextBox = False
            elif event.type == pygame.MOUSEBUTTONUP:
                tryPy_manager.check_for_snap(selectedBlock)
                dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if selectedBlock and dragging:
                    selectedBlock.move(*event.rel)
            elif event.type == pygame.KEYDOWN:
                if isActiveTextBox:
                    if event.key == pygame.K_BACKSPACE:
                        selectedBlock.backspace()
                    else:
                        selectedBlock.update_text(event.unicode)
                elif event.key == pygame.K_s:
                    tryPy_manager.run_blocks()
                elif event.key == pygame.K_r:
                    tryPy_manager.reset()

            # clock.tick() # for showing fps
            # print(clock.get_fps())
            tryPy_manager.render_blocks()


if __name__=="__main__":
    main()