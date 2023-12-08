from Entity.Entity import Entity
from constants import STENCH_IMAGE


class Stench(Entity):
    def __init__(self, row, col):
        super().__init__(row, col, STENCH_IMAGE)
