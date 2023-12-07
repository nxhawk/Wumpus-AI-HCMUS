import pygame

from constants import WIDTH, GREEN


class Message(object):
    def __init__(self, message):
        self.cs_font_1 = pygame.font.SysFont('Comic Sans MS', 30)
        self.x = WIDTH - WIDTH//5
        self.y = 50
        self.message = message.replace("_", " ")

    def draw(self, screen):
        my_text = self.cs_font_1.render(self.message, False, GREEN)
        text_width = my_text.get_width()
        screen.blit(my_text, (self.x - text_width//2, self.y))
