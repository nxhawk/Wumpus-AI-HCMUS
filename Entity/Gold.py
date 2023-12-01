import pygame

from constants import MARGIN, SPACING_CELL, CELL_SIZE, GOLD_IMAGE
from utils import Utils


class Gold(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.image = Utils.load_image_alpha(GOLD_IMAGE)
        self.rect = self.image.get_rect()
        self.rect.top = row * CELL_SIZE + MARGIN["TOP"] + (row + 1) * SPACING_CELL
        self.rect.left = col * CELL_SIZE + MARGIN["LEFT"] + (col + 1) * SPACING_CELL

    def draw(self, screen: pygame):
        screen.blit(self.image, self.rect)
