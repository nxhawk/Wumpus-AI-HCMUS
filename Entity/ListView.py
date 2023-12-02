import pygame

from constants import GREY, WHITE, RED, WIDTH


class ListView:
    def __init__(self):
        self.font_size = 18
        self.font = pygame.font.Font(None, self.font_size)
        self.width = 200
        self.height = 300
        self.color = WHITE
        self.marginBottom = self.font_size//2+2
        self.padding = 0
        self.left = WIDTH - 200
        self.top = 100

        self.scroll_position = 0
        self.scroll_speed = 5
        self.scrollbar_width = 16
        self.scrollbar_rect = pygame.Rect(self.left, self.top, self.scrollbar_width, self.height)

        # content of list view
        self.items = [f"Item {i}" for i in range(1, 50)]

    def draw_list_view(self, screen: pygame):
        for i, item in enumerate(self.items):
            text = self.font.render(item, True, self.color)
            text_rect = text.get_rect()
            text_rect.topleft = (self.left-100, self.top + i * self.marginBottom - self.scroll_position)
            if text_rect.topleft[1] < self.top or text_rect.topleft[1] > self.top+self.height - self.font_size//2:
                continue
            screen.blit(text, text_rect)

    def draw_scrollbar(self, screen):
        pygame.draw.rect(screen, GREY, self.scrollbar_rect)

        handle_position = ((self.scroll_position / (len(self.items) * self.marginBottom - self.height)) *
                           (self.height - self.scrollbar_width)) + self.top
        handle_rect = pygame.Rect(self.left, handle_position, self.scrollbar_width,
                                  self.scrollbar_width)
        pygame.draw.rect(screen, RED, handle_rect)

    def scroll_bottom(self):
        self.scroll_position = len(self.items) * self.marginBottom - self.height

    def scroll_up(self):
        self.scroll_position = max(0, self.scroll_position - self.scroll_speed)

    def scroll_down(self):
        self.scroll_position = min(len(self.items) * self.marginBottom - self.height, self.scroll_position
                                   + self.scroll_speed)

    def add_item(self, content):
        self.items.append(content)

    def draw(self, screen):
        self.draw_list_view(screen)
        # self.draw_scrollbar(screen)
