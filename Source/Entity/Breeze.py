from Entity.Entity import Entity
from constants import BREEZE_IMAGE


class Breeze(Entity):
    def __init__(self, row, col):
        super().__init__(row, col, BREEZE_IMAGE)
