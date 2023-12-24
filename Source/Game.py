import sys

import pygame

from Entity.Board import Board
from Menu.Button import Button
from Menu.Button2 import Button2
from Menu.Item import Item
from Run.RandMap import random_Map
from constants import (NAME_WINDOW, FPS, WIDTH, HEIGHT, ICON_NAME, BLACK, MESSAGE_WINDOW, MARGIN, BG_IMAGE, FONT_3, RED,
                       WHITE, FONT_1, NAME_ITEM, YELLOW, NUMBER_CELL)

# --------------------- initial pygame -----------------------------
pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption(NAME_WINDOW)
pygame.display.set_icon(pygame.image.load(ICON_NAME))
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# -------------------- end initial pygame --------------------------


# ---------------------- create global data --------------------------------


# ---------------------- end create global data ----------------------------


def about_us():
    my_font = pygame.font.Font(FONT_3, 120)
    text_surface = my_font.render('ABOUT US', False, RED)
    screen.blit(text_surface, ((WIDTH - text_surface.get_width()) // 2, 30))

    my_font = pygame.font.Font(FONT_1, 50)
    default_surface = my_font.render('21120439 - Bùi Minh Duy', False, WHITE)
    text_surface = my_font.render('21120439 - Bùi Minh Duy', False, WHITE)
    screen.blit(text_surface, ((WIDTH - default_surface.get_width()) // 2, 30 + (HEIGHT - 30) // 4))
    text_surface = my_font.render('21120447 - Nguyễn Nhật Hào', False, WHITE)
    screen.blit(text_surface, ((WIDTH - default_surface.get_width()) // 2, 30 + (HEIGHT - 30) // 4 + 80))
    text_surface = my_font.render('21120453 - Tô Phương Hiếu', False, WHITE)
    screen.blit(text_surface, ((WIDTH - default_surface.get_width()) // 2, 30 + (HEIGHT - 30) // 4 + 160))
    text_surface = my_font.render('21120457 - Lê Minh Hoàng', False, WHITE)
    screen.blit(text_surface, ((WIDTH - default_surface.get_width()) // 2, 30 + (HEIGHT - 30) // 4 + 240))


def quit_click():
    pygame.quit()
    sys.exit(0)


class Game:
    def __init__(self):
        self.running = False
        self.running_menu = True
        self.board = None
        self.status = "START_MENU"
        self.delay = 10
        self.map_name = None
        self.result_name = None
        self.clicked = False
        self.current_item = 0

        bg = pygame.image.load(BG_IMAGE)
        self.bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

        # Screen Home
        self.btnStart = Button2((WIDTH - 350) // 2, (HEIGHT - 100) // 2 - HEIGHT // 6, 350, 100, screen,
                                60, 'START', self.start_click, WHITE)
        self.btnIntroduce = Button2((WIDTH - 350) // 2, (HEIGHT - 100) // 2 + 15, 350, 100, screen,
                                    60, 'INTRODUCE', self.introduce_click, WHITE)
        self.btnAbout = Button2((WIDTH - 350) // 2, (HEIGHT - 100) // 2 + HEIGHT // 6 + 30, 350, 100, screen,
                                60, 'ABOUT US', self.about_click, WHITE)
        self.btnQuit = Button2((WIDTH - 350) // 2, (HEIGHT - 100) // 2 + HEIGHT // 3 + 45, 350, 100, screen,
                               60, 'QUIT', quit_click, WHITE)

        # Screen Choose map
        self.btnBackHome = Button2(20, HEIGHT - 120, 200, 100, screen,
                                   60, 'BACK', self.back_home_click, WHITE)

        self.btnMap1 = Button2((WIDTH - 300) // 2, (HEIGHT - 100) // 2 - HEIGHT // 5 * 2, 300, 100, screen,
                               60, 'MAP 1', self.choose_map_1, WHITE)
        self.btnMap2 = Button2((WIDTH - 300) // 2, (HEIGHT - 100) // 2 - HEIGHT // 5 * 1, 300, 100, screen,
                               60, 'MAP 2', self.choose_map_2, WHITE)
        self.btnMap3 = Button2((WIDTH - 300) // 2, (HEIGHT - 100) // 2, 300, 100, screen,
                               60, 'MAP 3', self.choose_map_3, WHITE)
        self.btnMap4 = Button2((WIDTH - 300) // 2, (HEIGHT - 100) // 2 + HEIGHT // 5 * 1, 300, 100, screen,
                               60, 'MAP 4', self.choose_map_4, WHITE)
        self.btnMap5 = Button2((WIDTH - 300) // 2, (HEIGHT - 100) // 2 + HEIGHT // 5 * 2, 300, 100, screen,
                               60, 'MAP 5', self.choose_map_5, WHITE)
        # Random map
        self.btnMapRand = Button2(WIDTH - 350, (HEIGHT - 100) // 2 - HEIGHT // 5 * 1, 300, 100, screen,
                                  60, 'RANDOM', self.choose_rand_map, WHITE)

        # Screen End Game
        self.btnBack = None
        self.btnRestart = None

        # Introduce screen
        self.btnNext = Button2(WIDTH - 200, (HEIGHT - 100) // 2, 100, 100, screen,
                               100, '>', self.next_click, WHITE)
        self.btnPrev = Button2(100, (HEIGHT - 100) // 2, 100, 100, screen,
                               100, '<', self.prev_click, WHITE)

    def next_click(self):
        if self.clicked:
            self.current_item = (self.current_item + 1) % len(NAME_ITEM)

    def prev_click(self):
        if self.clicked:
            self.current_item -= 1
            if self.current_item < 0:
                self.current_item = self.current_item + len(NAME_ITEM)

    def introduce(self):
        my_font = pygame.font.Font(FONT_3, 120)
        text_surface = my_font.render('INTRODUCE', False, RED)
        screen.blit(text_surface, ((WIDTH - text_surface.get_width()) // 2, 30))

        self.btnNext.process()
        self.btnPrev.process()

        # show text info this item
        my_font = pygame.font.Font(FONT_3, 100)
        text_item = my_font.render(NAME_ITEM[self.current_item], False, YELLOW)
        screen.blit(text_item, ((WIDTH - text_item.get_width()) // 2, (HEIGHT - text_item.get_height()) - 130))

        # show image info this item
        item = Item(WIDTH // 2, HEIGHT // 2 - 20, NAME_ITEM[self.current_item])
        item.draw(screen)

    def initBtnEndGame(self):
        self.btnBack = Button(MESSAGE_WINDOW['LEFT'] + 20, MESSAGE_WINDOW['BOTTOM'] - 100, 200, 60, screen,
                              40, 'BACK', self.back_click)
        self.btnRestart = Button(WIDTH - 220, MESSAGE_WINDOW['BOTTOM'] - 100, 200, 60, screen,
                                 40, 'RESTART', self.restart_click)

    def choose_map_1(self):
        if self.clicked:
            self.map_name = "map1.txt"
            self.result_name = "result1.txt"
            self.status = "RUN_GAME"

    def choose_map_2(self):
        if self.clicked:
            self.map_name = "map2.txt"
            self.result_name = "result2.txt"
            self.status = "RUN_GAME"

    def choose_map_3(self):
        if self.clicked:
            self.map_name = "map3.txt"
            self.result_name = "result3.txt"
            self.status = "RUN_GAME"

    def choose_map_4(self):
        if self.clicked:
            self.map_name = "map4.txt"
            self.result_name = "result4.txt"
            self.status = "RUN_GAME"

    def choose_map_5(self):
        if self.clicked:
            self.map_name = "map5.txt"
            self.result_name = "result5.txt"
            self.status = "RUN_GAME"

    def choose_rand_map(self):
        if self.clicked:
            self.map_name = "randMap.txt"
            random_Map(NUMBER_CELL, self.map_name)
            self.result_name = "resultRandMap.txt"
            self.status = "RUN_GAME"

    def move(self):
        if not self.board.move():
            self.status = "END_GAME"

    def back_click(self):
        self.status = "CHOOSE_MAP"
        self.running_menu = True
        self.running = False
        self.menu()

    def back_home_click(self):
        if self.clicked:
            self.status = "START_MENU"

    def introduce_click(self):
        if self.clicked:
            self.current_item = 0
            self.status = "INTRODUCE_MENU"

    def about_click(self):
        if self.clicked:
            self.status = "ABOUT_US_MENU"

    def start_click(self):
        if self.clicked:
            self.status = "CHOOSE_MAP"
            self.clicked = False

    def restart_click(self):
        MARGIN["LEFT"] = 0
        self.status = "RUN_GAME"
        self.delay = 10
        self.board = Board(self.map_name, self.result_name)

    def run(self) -> None:
        self.clicked = False
        while self.running:
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
                    self.running = False
                    self.running_menu = True
                    self.status = "START_MENU"
                    self.menu()
                    # TODO: show menu latest
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

    def menu(self):
        my_font = pygame.font.Font(FONT_3, 120)
        text_surface = my_font.render('WUMPUS WORLD', False, RED)
        while self.running_menu:
            self.clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running_menu = False
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True

            # re-draw window
            screen.blit(self.bg, (0, 0))
            if self.status != "START_MENU":
                self.btnBackHome.process()
            if self.status == "START_MENU":
                screen.blit(text_surface, ((WIDTH - text_surface.get_width()) // 2, 30))
                self.btnStart.process()
                self.btnIntroduce.process()
                self.btnAbout.process()
                self.btnQuit.process()
            elif self.status == "CHOOSE_MAP":
                self.btnMap1.process()
                self.btnMap2.process()
                self.btnMap3.process()
                self.btnMap4.process()
                self.btnMap5.process()
                self.btnMapRand.process()
            elif self.status == "INTRODUCE_MENU":
                self.introduce()
            elif self.status == "ABOUT_US_MENU":
                about_us()
            elif self.status == "RUN_GAME":
                self.running_menu = False
                self.running = True
                MARGIN['LEFT'] = 0
                self.board = Board(self.map_name, self.result_name)
                self.initBtnEndGame()
                self.run()

            pygame.display.flip()
            clock.tick(FPS)
            # ----------------------------
