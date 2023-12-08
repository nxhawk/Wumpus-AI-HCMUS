from Entity.Entity import Entity
from constants import GOLD_IMAGE


class Gold(Entity):
    def __init__(self, row, col):
        super().__init__(row, col, GOLD_IMAGE)
