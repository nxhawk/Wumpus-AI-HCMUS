import pygame

from Entity.Board import Board
from Entity.ListView import ListView
from constants import NAME_WINDOW, FPS, WIDTH, HEIGHT, ICON_NAME, BLACK

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
        self.listView = ListView()

    def move(self):
        self.board.move()

    def run(self) -> None:
        delay = 100
        global running
        while running:
            # re-draw window
            screen.fill(BLACK)
            self.board.draw(screen)
            self.listView.scroll_bottom()
            self.listView.draw(screen)
            pygame.display.flip()
            clock.tick(FPS)
            # ----------------------------

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # TODO: show menu latest
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        self.listView.scroll_up()
                    elif event.button == 5:
                        self.listView.scroll_down()

            # delay game
            if delay > 0:
                delay -= 1
                continue

            # Agent move
            self.move()
