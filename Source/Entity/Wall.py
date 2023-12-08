from Entity.Entity import Entity
from constants import WALL_IMAGE


class Wall(Entity):
    def __init__(self, row, col):
        super().__init__(row, col, WALL_IMAGE)
