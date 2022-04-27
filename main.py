# import the pygame module, so you can use it
import pygame
import pygame.freetype
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

    def check_textBox_collisions(self, selectedBlock, x, y):
        if selectedBlock.within_textBox_bounds(x, y):
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
        return snap_collisions if len(snap_collisions) > 0 else [None]

    def check_for_snap(self, selectedBlock):
        if selectedBlock is None:
            return
        snap_candidates = self.get_snap_collisions(selectedBlock)
        if snap_candidates[0] is not None:
            selectedBlock.snap(snap_candidates[0])
        else:
            selectedBlock.unsnap()

def setup_screen(title, x, y):
    pygame.init()   # initialize the pygame module
    pygame.display.set_caption(title)
    screen = pygame.display.set_mode((x,y))
    return screen

# define a main function
def main():
    screen = setup_screen(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT)
    tryPy_manager = BlockManager(screen)

    tryPy_manager.add_block(Block(0, 0, 100, 100))
    tryPy_manager.add_block(Start(100, 0, 100, 100))
    tryPy_manager.add_block(If(200, 0, 100, 100))
    tryPy_manager.add_block(While(300, 0, 100, 100))
    tryPy_manager.add_block(For(400, 0, 100, 100))
    tryPy_manager.add_block(Break(500, 0, 100, 100))
    tryPy_manager.add_block(Print(600, 0, 100, 100))

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
                if selectedBlock and selectedBlock.has_condition(): 
                    selectedBlock.disactivate_textBox()
                selectedBlock = tryPy_manager.check_block_collisions(*event.pos)[0]
                if selectedBlock and selectedBlock.has_condition():
                    isActiveTextBox = tryPy_manager.check_textBox_collisions(selectedBlock, *event.pos) 
                else:
                    isActiveTextBox = False
            elif event.type == pygame.MOUSEBUTTONUP:
                tryPy_manager.check_for_snap(selectedBlock)
                dragging = False
                #selectedBlock = None
                #isActiveTextBox= False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    selectedBlock.move(*event.rel)
            elif event.type == pygame.KEYDOWN:
                if isActiveTextBox:
                    if event.key == pygame.K_BACKSPACE:
                        selectedBlock.backspace()
                    else:
                        selectedBlock.update_text(event.unicode)
            tryPy_manager.render_blocks()


if __name__=="__main__":
    main()