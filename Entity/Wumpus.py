from Entity.Entity import Entity
from constants import WUMPUS_IMAGE


class Wumpus(Entity):
    def __init__(self, row, col):
        super().__init__(row, col, WUMPUS_IMAGE)
