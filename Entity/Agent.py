import utils
from Entity.Entity import Entity
from constants import CELL_SIZE, MARGIN, SPACING_CELL, AGENT_IMAGE
from utils import Utils


class Agent(Entity):
    def __init__(self, row, col, N):
        super().__init__(row, col, AGENT_IMAGE[0])
        self.N = N

    def setRC(self, row, col):
        if not utils.Utils.isValid(row, col, self.N):
            return

        if row < self.row:
            self.image = Utils.load_image_alpha(AGENT_IMAGE[2])
        elif row > self.row:
            self.image = Utils.load_image_alpha(AGENT_IMAGE[3])

        if col < self.col:
            self.image = Utils.load_image_alpha(AGENT_IMAGE[1])
        elif col > self.col:
            self.image = Utils.load_image_alpha(AGENT_IMAGE[0])

        self.row = row
        self.col = col

        self.rect = self.image.get_rect()
        self.rect.top = row * CELL_SIZE + MARGIN["TOP"] + (row + 1) * SPACING_CELL
        self.rect.left = col * CELL_SIZE + MARGIN["LEFT"] + (col + 1) * SPACING_CELL
