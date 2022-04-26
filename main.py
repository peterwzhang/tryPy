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

    def check_collisions(self, x, y):
        # handle if multiple blocks on top of each other
        for block in self.blocks:
            if block.within_bounds(x, y):
                return block
        return None


def setup_screen(title, x, y):
    pygame.init()   # initialize the pygame module
    pygame.display.set_caption(title)
    screen = pygame.display.set_mode((x,y))
    return screen

# define a main function
def main():
    tryPy_manager = BlockManager(setup_screen(SCREEN_TITLE, SCREEN_WIDTH, SCREEN_HEIGHT))


    tryPy_manager.add_block(Block(0, 0, 100, 100))
    tryPy_manager.add_block(Conditional(100, 0, 100, 100))
    tryPy_manager.add_block(Loop(200, 0, 100, 100))
    tryPy_manager.add_block(Start(300, 0, 100, 100))

    # variable for main game loop + mouse drag handling
    running = True
    selectedBlock = None
    dragging = False
    # main loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                dragging = True
                selectedBlock = tryPy_manager.check_collisions(*event.pos)
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                selectedBlock = None
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    selectedBlock.move(*event.rel)
            tryPy_manager.render_blocks()


if __name__=="__main__":
    main()