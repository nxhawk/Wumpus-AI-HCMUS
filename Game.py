import pygame

from Entity.Board import Board
from constants import NAME_WINDOW, FPS, WIDTH, HEIGHT, ICON_NAME, BLACK, BLUE

# --------------------- initial pygame -----------------------------
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption(NAME_WINDOW)
pygame.display.set_icon(pygame.image.load(ICON_NAME))
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# -------------------- end initial pygame --------------------------

# ---------------------- create global data --------------------------------
running = True


# ---------------------- end create global data ----------------------------


class Game:
    def __init__(self):
        self.board = Board()

    def run(self) -> None:
        delay = 100
        global running
        while running:
            # re-draw window
            self.board.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
            # ----------------------------

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # TODO: show menu latest
                    return

            # delay game
            if delay > 0:
                delay -= 1
                continue