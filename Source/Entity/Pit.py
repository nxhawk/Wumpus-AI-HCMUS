from Entity.Entity import Entity
from constants import PIT_IMAGE


class Pit(Entity):
    def __init__(self, row, col):
        super().__init__(row, col, PIT_IMAGE)
