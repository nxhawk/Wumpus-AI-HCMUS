import pygame

from Entity.Board import Board
from Menu.Button import Button
from constants import NAME_WINDOW, FPS, WIDTH, HEIGHT, ICON_NAME, BLACK, MESSAGE_WINDOW, MARGIN

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
        self.status = "RUN_GAME"
        self.delay = 10

        self.btnBack = Button(MESSAGE_WINDOW['LEFT'] + 20, MESSAGE_WINDOW['BOTTOM'] - 100, 200, 60, screen,
                              40, 'BACK', self.back_click)
        self.btnRestart = Button(WIDTH - 220, MESSAGE_WINDOW['BOTTOM'] - 100, 200, 60, screen,
                                 40, 'RESTART', self.restart_click)

    def move(self):
        if not self.board.move():
            self.status = "END_GAME"

    def back_click(self):
        pass

    def restart_click(self):
        MARGIN["LEFT"] = 0
        self.status = "RUN_GAME"
        self.delay = 10
        self.board = Board()

    def run(self) -> None:
        global running
        while running:
            # re-draw window
            screen.fill(BLACK)
            self.board.draw(screen)
            if self.status == 'END_GAME':
                self.btnBack.process()
                self.btnRestart.process()

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
                        self.board.scroll_up()
                    elif event.button == 5:
                        self.board.scroll_down()

            # delay game
            if self.delay > 0:
                self.delay -= 1
                continue

            # Agent move
            self.move()
